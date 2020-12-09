from pytest_mock import MockerFixture
from pyfenstein3d.engine import Server
from pyfenstein3d.engine import Map2d
from pyfenstein3d.engine import Wall


def map2d_update_side_effect():
    print("cls")


def test_init(mocker: MockerFixture):
    server = Server()
    open_mock = mocker.patch('builtins.open', mocker.mock_open(read_data='010203'))
    mocker.patch("pyfenstein3d.engine.server.FRAME_PER_SECONDS", 10)
    map2d = Map2d([Wall(1, 2, 10)])
    map2d_create_with_pattern_mock = mocker.patch.object(Map2d, "create_with_pattern")
    map2d_create_with_pattern_mock.return_value = map2d
    map2d_update = mocker.patch.object(map2d, "update")
    map2d_update.side_effect = lambda: server.stop_game()
    server.load_map_file("teste")
    server.start_game()

    open_mock.assert_called_once_with("teste", "r")
    map2d_update.assert_called_once()
