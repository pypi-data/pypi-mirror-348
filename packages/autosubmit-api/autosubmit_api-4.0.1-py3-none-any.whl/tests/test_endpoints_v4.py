from datetime import datetime, timedelta
from http import HTTPStatus
import random
from uuid import uuid4
from flask.testing import FlaskClient
import jwt
import pytest
from autosubmit_api import config
from autosubmit_api.views.v4 import PAGINATION_LIMIT_DEFAULT, ExperimentJobsViewOptEnum
from tests.utils import custom_return_value


class TestCASV2Login:
    endpoint = "/v4/auth/cas/v2/login"

    def test_redirect(
        self, fixture_client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        random_url = f"https://${str(uuid4())}/"
        monkeypatch.setattr(config, "CAS_SERVER_URL", random_url)
        assert random_url == config.CAS_SERVER_URL

        response = fixture_client.get(self.endpoint)

        assert response.status_code == HTTPStatus.FOUND
        assert config.CAS_SERVER_URL in response.location

    def test_invalid_client(
        self, fixture_client: FlaskClient, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            "autosubmit_api.views.v4.validate_client", custom_return_value(False)
        )
        response = fixture_client.get(self.endpoint, query_string={"service": "asd"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestJWTVerify:
    endpoint = "/v4/auth/verify-token"

    def test_unauthorized_no_token(self, fixture_client: FlaskClient):
        response = fixture_client.get(self.endpoint)
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert resp_obj.get("authenticated") is False
        assert resp_obj.get("user") is None

    def test_unauthorized_random_token(self, fixture_client: FlaskClient):
        random_token = str(uuid4())
        response = fixture_client.get(
            self.endpoint, headers={"Authorization": random_token}
        )
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert resp_obj.get("authenticated") is False
        assert resp_obj.get("user") is None

    def test_authorized(self, fixture_client: FlaskClient):
        random_user = str(uuid4())
        payload = {
            "user_id": random_user,
            "sub": random_user,
            "iat": int(datetime.now().timestamp()),
            "exp": (
                datetime.utcnow() + timedelta(seconds=config.JWT_EXP_DELTA_SECONDS)
            ),
        }
        jwt_token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)

        response = fixture_client.get(
            self.endpoint, headers={"Authorization": jwt_token}
        )
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert resp_obj.get("authenticated") is True
        assert resp_obj.get("user") == random_user


class TestExperimentList:
    endpoint = "/v4/experiments"

    def test_page_size(self, fixture_client: FlaskClient):
        # Default page size
        response = fixture_client.get(self.endpoint)
        resp_obj: dict = response.get_json()
        assert resp_obj["pagination"]["page_size"] == PAGINATION_LIMIT_DEFAULT

        # Any page size
        page_size = random.randint(2, 100)
        response = fixture_client.get(
            self.endpoint, query_string={"page_size": page_size}
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["pagination"]["page_size"] == page_size

        # Unbounded page size
        response = fixture_client.get(self.endpoint, query_string={"page_size": -1})
        resp_obj: dict = response.get_json()
        assert resp_obj["pagination"]["page_size"] is None
        assert (
            resp_obj["pagination"]["page_items"]
            == resp_obj["pagination"]["total_items"]
        )
        assert resp_obj["pagination"]["page"] == 1
        assert resp_obj["pagination"]["page"] == resp_obj["pagination"]["total_pages"]


class TestExperimentDetail:
    endpoint = "/v4/experiments/{expid}"

    def test_detail(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["id"] == 1
        assert resp_obj["name"] == expid
        assert (
            isinstance(resp_obj["description"], str)
            and len(resp_obj["description"]) > 0
        )
        assert (
            isinstance(resp_obj["autosubmit_version"], str)
            and len(resp_obj["autosubmit_version"]) > 0
        )


class TestExperimentJobs:
    endpoint = "/v4/experiments/{expid}/jobs"

    def test_quick(self, fixture_client: FlaskClient):
        expid = "a003"

        response = fixture_client.get(
            self.endpoint.format(expid=expid),
            query_string={"view": ExperimentJobsViewOptEnum.QUICK.value},
        )
        resp_obj: dict = response.get_json()

        assert len(resp_obj["jobs"]) == 8

        for job in resp_obj["jobs"]:
            assert isinstance(job, dict) and len(job.keys()) == 2
            assert isinstance(job["name"], str) and job["name"].startswith(expid)
            assert isinstance(job["status"], str)

    def test_base(self, fixture_client: FlaskClient):
        expid = "a003"

        response = fixture_client.get(
            self.endpoint.format(expid=expid),
            query_string={"view": ExperimentJobsViewOptEnum.BASE.value},
        )
        resp_obj: dict = response.get_json()

        assert len(resp_obj["jobs"]) == 8

        for job in resp_obj["jobs"]:
            assert isinstance(job, dict) and len(job.keys()) > 2
            assert isinstance(job["name"], str) and job["name"].startswith(expid)
            assert isinstance(job["status"], str)


class TestExperimentWrappers:
    endpoint = "/v4/experiments/{expid}/wrappers"

    def test_wrappers(self, fixture_client: FlaskClient):
        expid = "a6zj"

        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["wrappers"], list)
        assert len(resp_obj["wrappers"]) == 1

        for wrapper in resp_obj["wrappers"]:
            assert isinstance(wrapper, dict)
            assert isinstance(wrapper["job_names"], list)
            assert isinstance(wrapper["wrapper_name"], str) and wrapper[
                "wrapper_name"
            ].startswith(expid)


class TestExperimentFSConfig:
    endpoint = "/v4/experiments/{expid}/filesystem-config"

    def test_fs_config(self, fixture_client: FlaskClient):
        expid = "a6zj"

        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["config"], dict)
        assert (
            isinstance(resp_obj["config"]["contains_nones"], bool)
            and not resp_obj["config"]["contains_nones"]
        )
        assert isinstance(resp_obj["config"]["JOBS"], dict)
        assert isinstance(resp_obj["config"]["WRAPPERS"], dict)
        assert isinstance(resp_obj["config"]["WRAPPERS"]["WRAPPER_V"], dict)

    def test_fs_config_v3_retro(self, fixture_client: FlaskClient):
        expid = "a3tb"

        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["config"], dict)

        ALLOWED_CONFIG_KEYS = ["conf", "exp", "jobs", "platforms", "proj"]
        assert len(resp_obj["config"].keys()) == len(ALLOWED_CONFIG_KEYS) + 1
        assert (
            isinstance(resp_obj["config"]["contains_nones"], bool)
            and not resp_obj["config"]["contains_nones"]
        )
        for key in ALLOWED_CONFIG_KEYS:
            assert key in resp_obj["config"]
            assert isinstance(resp_obj["config"][key], dict)


class TestExperimentRuns:
    endpoint = "/v4/experiments/{expid}/runs"

    @pytest.mark.parametrize("expid, num_runs", [("a6zj", 1), ("a3tb", 51)])
    def test_runs(self, expid: str, num_runs: int, fixture_client: FlaskClient):
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["runs"], list)
        assert len(resp_obj["runs"]) == num_runs

        for run in resp_obj["runs"]:
            assert isinstance(run, dict)
            assert isinstance(run["run_id"], int)
            assert isinstance(run["start"], str) or run["start"] is None
            assert isinstance(run["finish"], str) or run["finish"] is None


class TestExperimentRunConfig:
    endpoint = "/v4/experiments/{expid}/runs/{run_id}/config"

    def test_run_config(self, fixture_client: FlaskClient):
        expid = "a6zj"
        run_id = 1

        response = fixture_client.get(self.endpoint.format(expid=expid, run_id=run_id))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["config"], dict)
        assert (
            isinstance(resp_obj["config"]["contains_nones"], bool)
            and not resp_obj["config"]["contains_nones"]
        )
        assert isinstance(resp_obj["config"]["JOBS"], dict)
        assert isinstance(resp_obj["config"]["WRAPPERS"], dict)
        assert isinstance(resp_obj["config"]["WRAPPERS"]["WRAPPER_V"], dict)

    @pytest.mark.parametrize("run_id", [51, 48, 31])
    def test_run_config_v3_retro(self, run_id: int, fixture_client: FlaskClient):
        expid = "a3tb"

        response = fixture_client.get(self.endpoint.format(expid=expid, run_id=run_id))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj, dict)
        assert isinstance(resp_obj["config"], dict)

        ALLOWED_CONFIG_KEYS = ["conf", "exp", "jobs", "platforms", "proj"]
        assert len(resp_obj["config"].keys()) == len(ALLOWED_CONFIG_KEYS) + 1
        assert (
            isinstance(resp_obj["config"]["contains_nones"], bool)
            and not resp_obj["config"]["contains_nones"]
        )
        for key in ALLOWED_CONFIG_KEYS:
            assert key in resp_obj["config"]
            assert isinstance(resp_obj["config"][key], dict)
