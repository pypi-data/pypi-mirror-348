from datetime import datetime
import os
import time
from typing import Dict, List

from sqlalchemy import select
from autosubmit_api.bgtasks.bgtask import BackgroundTaskTemplate
from autosubmit_api.database import tables
from autosubmit_api.database.common import (
    create_autosubmit_db_engine,
    create_as_times_db_engine,
    create_main_db_conn,
)
from autosubmit_api.database.models import ExperimentModel
from autosubmit_api.experiment.common_requests import _is_exp_running
from autosubmit_api.history.database_managers.database_models import RunningStatus
from autosubmit_api.persistance.experiment import ExperimentPaths


class StatusUpdater(BackgroundTaskTemplate):
    id = "TASK_STTSUPDTR"
    trigger_options = {"trigger": "interval", "minutes": 5}

    @classmethod
    def _clear_missing_experiments(cls):
        """
        Clears the experiments that are not in the experiments table
        """
        with create_main_db_conn() as conn:
            try:
                del_stmnt = tables.experiment_status_table.delete().where(
                    tables.experiment_status_table.c.exp_id.not_in(
                        select(tables.experiment_table.c.id)
                    )
                )
                conn.execute(del_stmnt)
                conn.commit()
            except Exception as exc:
                conn.rollback()
                cls.logger.error(
                    f"[{cls.id}] Error while clearing missing experiments status: {exc}"
                )

    @classmethod
    def _get_experiments(cls) -> List[ExperimentModel]:
        """
        Get the experiments list
        """
        with create_autosubmit_db_engine().connect() as conn:
            query_result = conn.execute(tables.experiment_table.select()).all()
        return [ExperimentModel.model_validate(row._mapping) for row in query_result]

    @classmethod
    def _get_current_status(cls) -> Dict[str, str]:
        """
        Get the current status of the experiments
        """
        with create_as_times_db_engine().connect() as conn:
            query_result = conn.execute(tables.experiment_status_table.select()).all()
        return {row.name: row.status for row in query_result}

    @classmethod
    def _check_exp_running(cls, expid: str) -> bool:
        """
        Decide if the experiment is running
        """
        MAX_PKL_AGE = 600  # 10 minutes
        MAX_PKL_AGE_EXHAUSTIVE = 3600  # 1 hour

        is_running = False
        try:
            pkl_path = ExperimentPaths(expid).job_list_pkl
            pkl_age = int(time.time()) - int(os.stat(pkl_path).st_mtime)

            if pkl_age < MAX_PKL_AGE:  # First running check
                is_running = True
            elif pkl_age < MAX_PKL_AGE_EXHAUSTIVE:  # Exhaustive check
                _, _, _flag, _, _ = _is_exp_running(expid)  # Exhaustive validation
                if _flag:
                    is_running = True
        except Exception as exc:
            cls.logger.error(
                f"[{cls.id}] Error while checking experiment {expid}: {exc}"
            )

        return is_running

    @classmethod
    def _update_experiment_status(cls, experiment: ExperimentModel, is_running: bool):
        with create_as_times_db_engine().connect() as conn:
            try:
                del_stmnt = tables.experiment_status_table.delete().where(
                    tables.experiment_status_table.c.exp_id == experiment.id
                )
                ins_stmnt = tables.experiment_status_table.insert().values(
                    exp_id=experiment.id,
                    name=experiment.name,
                    status=(
                        RunningStatus.RUNNING
                        if is_running
                        else RunningStatus.NOT_RUNNING
                    ),
                    seconds_diff=0,
                    modified=datetime.now().isoformat(sep="-", timespec="seconds"),
                )
                conn.execute(del_stmnt)
                conn.execute(ins_stmnt)
                conn.commit()
            except Exception as exc:
                conn.rollback()
                cls.logger.error(
                    f"[{cls.id}] Error while doing database operations on experiment {experiment.name}: {exc}"
                )

    @classmethod
    def procedure(cls):
        """
        Updates STATUS of experiments.
        """
        cls._clear_missing_experiments()

        # Read experiments table
        exp_list = cls._get_experiments()

        # Read current status of all experiments
        current_status = cls._get_current_status()

        # Check every experiment status & update
        for experiment in exp_list:
            is_running = cls._check_exp_running(experiment.name)
            new_status = (
                RunningStatus.RUNNING if is_running else RunningStatus.NOT_RUNNING
            )
            if (
                current_status.get(experiment.name, RunningStatus.NOT_RUNNING)
                != new_status
            ):
                cls.logger.info(
                    f"[{cls.id}] Updating status of {experiment.name} to {new_status}"
                )
                cls._update_experiment_status(experiment, is_running)
