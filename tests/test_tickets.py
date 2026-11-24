from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

import app.database as db
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """テストごとに一時DBを作成してクリーンな状態で実行する"""
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    db.init_db()
    yield


def test_create_and_get_ticket():
    # SPEC 3.2: 正常作成（priority省略時は初期値 LOW）
    res = client.post("/api/tickets", json={"title": "テストタスク", "assignee": "山田"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "テストタスク"
    assert data["status"] == "TODO"
    assert data["priority"] == "LOW"

    # SPEC 3.1: 一覧画面表示
    html_res = client.get("/")
    assert html_res.status_code == 200
    assert "テストタスク" in html_res.text
    assert "LOW" in html_res.text


def test_create_ticket_with_priority():
    # SPEC 2 / 3.2: HIGH, MEDIUM, LOW の作成と不正値(422)の検証
    for priority in ("HIGH", "MEDIUM", "LOW"):
        res = client.post(
            "/api/tickets",
            json={"title": f"{priority}タスク", "assignee": "山田", "priority": priority},
        )
        assert res.status_code == 201
        assert res.json()["priority"] == priority

    res_invalid = client.post(
        "/api/tickets",
        json={"title": "不正優先度", "assignee": "山田", "priority": "URGENT"},
    )
    assert res_invalid.status_code == 422


def test_validation_error():
    # SPEC 3.2: 空白のみは422エラー
    res = client.post("/api/tickets", json={"title": "   ", "assignee": "山田"})
    assert res.status_code == 422


def test_status_transition_rule():
    # SPEC 3.3: DONE -> TODO の禁止遷移ルール検証
    res = client.post("/api/tickets", json={"title": "完了予定タスク", "assignee": "佐藤"})
    ticket_id = res.json()["id"]

    # TODO -> DONE はOK
    res_done = client.patch(f"/api/tickets/{ticket_id}", json={"status": "DONE"})
    assert res_done.status_code == 200

    # DONE -> TODO は400エラーになるべき
    res_back = client.patch(f"/api/tickets/{ticket_id}", json={"status": "TODO"})
    assert res_back.status_code == 400

    # DONE -> DOING はOK
    res_doing = client.patch(f"/api/tickets/{ticket_id}", json={"status": "DOING"})
    assert res_doing.status_code == 200


def test_delete_ticket_priority_rule():
    # SPEC 3.3 / 3.4: priority が HIGH のチケットは削除禁止（400）、MEDIUM/LOW は削除可能（204）
    res_high = client.post(
        "/api/tickets",
        json={"title": "緊急対応", "assignee": "田中", "priority": "HIGH"},
    )
    high_id = res_high.json()["id"]

    del_high = client.delete(f"/api/tickets/{high_id}")
    assert del_high.status_code == 400
    assert "緊急対応" in client.get("/").text

    res_med = client.post(
        "/api/tickets",
        json={"title": "通常対応", "assignee": "田中", "priority": "MEDIUM"},
    )
    med_id = res_med.json()["id"]

    del_med = client.delete(f"/api/tickets/{med_id}")
    assert del_med.status_code == 204
    assert "通常対応" not in client.get("/").text