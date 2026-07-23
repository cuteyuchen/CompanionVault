from companion_vault.skill_install import install_skill


def test_packaged_skill_install(tmp_path):
    output=install_skill(None,"generic","project",tmp_path)
    assert (output/"SKILL.md").exists()
    assert (output/"tools/normalize_chat.py").exists()
