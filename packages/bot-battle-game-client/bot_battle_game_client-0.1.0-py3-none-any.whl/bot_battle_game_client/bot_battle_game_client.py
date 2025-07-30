import json
import time
from logging import DEBUG, basicConfig, getLogger
from typing import Any, Dict, List, Literal, Optional

import httpx
from pydantic import BaseModel

from .env import BotBattleClientSettings

logger = getLogger("bot-battle-game-client")
basicConfig(level=DEBUG)


class GameStateResponse(BaseModel):
    player_moves: dict[int, Optional[Dict[str, Any]]]
    tick: int


class BotBattleGameClient:
    config: BotBattleClientSettings
    client: httpx.Client

    tick: int

    player_moves: Dict[int, Optional[Dict[str, Any]]]

    def __init__(self, config: Optional[BotBattleClientSettings] = None):
        if config is None:
            config = BotBattleClientSettings()
        self.config = config
        self.client = httpx.Client(
            base_url=f"{self.config.cgi_url}/{self.config.game_id}"
        )
        self.tick = -1
        self.player_moves = {}

    @property
    def players(self):
        return [player_id for player_id in range(self.config.player_count)]

    @classmethod
    def _raise_on_error(cls, response: httpx.Response):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(response.content)
            raise e

    def _update_client_state(self, game_state: GameStateResponse) -> bool:
        """
        Update client state from a response from the GCI. Return `True` if there was new data provided.
        """
        _return_val = self.tick != game_state.tick or json.dumps(
            self.player_moves, sort_keys=True
        ) != json.dumps(game_state.player_moves, sort_keys=True)
        self.tick = game_state.tick
        self.player_moves = game_state.player_moves
        return _return_val

    def start_game(
        self,
        player_public_states: Dict[int, Dict[str, Any]],
        players_accepting_moves: List[int],
    ):
        resp = self.client.post(
            "/start",
            json={
                "player_public_states": player_public_states,
                "players_accepting_moves": players_accepting_moves,
            },
        )
        self._raise_on_error(resp)
        self._update_client_state(GameStateResponse.model_validate(resp.json()))
        return

    def get_state(self) -> bool:
        """
        Retrieve state from the GCI return `True` if there are any updates.
        """
        logger.debug("Fetching state from GCI.")
        resp = self.client.get("/state")
        self._raise_on_error(resp)
        return self._update_client_state(GameStateResponse.model_validate(resp.json()))

    def wait_for_changes(self, delay: float = 0.25) -> Literal[True]:
        """
        Polls the GCI for game state blocking until changes are detected.

        After starting the game the main portion of the game logic should live within this loop.

        ```python
        while client.wait_for_changes():
            # Do game logic...

            # If game is over
            client.end_game()
            break

        ```
        """
        while not self.get_state():
            logger.debug(f"No changes detected. Waiting {delay} before fetching again.")
            time.sleep(delay)
        return True

    def reject_moves(self, player_move_rejections: Dict[int, str]):
        """
        Reject player moves with a reason. This will mutate the local game state and remove the player moves from this client.
        """
        response = self.client.post(
            "/reject", json={"player_move_rejections": player_move_rejections}
        )
        self._raise_on_error(response)
        for player_id in player_move_rejections:
            self.player_moves[player_id] = None

    def update_game(
        self,
        player_public_states: Dict[int, Dict[str, Any]],
        players_accepting_moves: List[int],
    ):
        """
        Send a state update to the GCI. This will cause the game to progress 1 tick.

        Call this once the players which were required to submit a move on this tick have done so.

        An individual player_public_state must be <128Kb when encoded as json.
        """
        resp = self.client.post(
            "/update",
            json={
                "player_public_states": player_public_states,
                "players_accepting_moves": players_accepting_moves,
            },
        )
        self._raise_on_error(resp)
        self._update_client_state(GameStateResponse.model_validate(resp.json()))
        return

    def end_game(self, winners: List[int]):
        """
        End the game. The program should exit after calling this.
        """
        resp = self.client.post("/end", json={"winners": winners})
        self._raise_on_error(resp)
        return
