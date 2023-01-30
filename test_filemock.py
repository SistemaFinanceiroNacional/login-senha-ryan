import os.path
import filemock

def test_filemock_can_be_created():
    archive = "test_filemock1.cat"
    assert not os.path.exists(archive)
    with filemock.tempFile(archive, "pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542"):
        assert os.path.exists(archive)

    assert not os.path.exists(archive)
