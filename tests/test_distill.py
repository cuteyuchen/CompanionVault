from pathlib import Path
import yaml
import pytest

from companion_vault.distill import build_candidate
from companion_vault.privacy import redact_text


def sample_chat(tmp_path: Path) -> Path:
    path=tmp_path/"chat.txt";lines=[]
    for i in range(12):
        lines.append(f"用户: 今天第{i}件事有点烦")
        lines.append(f"小雨: 先别急啊 你慢慢说{i}")
    path.write_text("\n".join(lines),encoding="utf-8");return path


def test_redaction():
    text=redact_text("电话13800138000 邮箱a@example.com https://example.com",[])
    assert "13800138000" not in text and "a@example.com" not in text


def test_distill_public_candidate(tmp_path):
    output=build_candidate(sample_chat(tmp_path),"小雨","xiaoyu","小雨",tmp_path/"out","public","authorized")
    persona=yaml.safe_load((output/"persona.yaml").read_text(encoding="utf-8"));examples=yaml.safe_load((output/"examples.yaml").read_text(encoding="utf-8"))
    assert persona["provenance"]["raw_content_committed"] is False
    assert len(examples["examples"])==10
    assert (output/".private/normalized.jsonl").exists()


def test_public_unknown_consent_rejected(tmp_path):
    with pytest.raises(ValueError): build_candidate(sample_chat(tmp_path),"小雨","xiaoyu","小雨",tmp_path/"out","public","unknown")


def test_unreviewed_candidate_is_not_publishable(tmp_path):
    from companion_vault.core import repo_root,validate_persona
    output=build_candidate(sample_chat(tmp_path),"小雨","xiaoyu","小雨",tmp_path/"out","public","authorized")
    assert any("human review" in error for error in validate_persona(output,repo_root()))
