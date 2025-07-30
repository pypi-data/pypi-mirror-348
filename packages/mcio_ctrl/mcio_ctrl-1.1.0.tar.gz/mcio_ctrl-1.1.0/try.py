import sys
from collections import defaultdict
from typing import Any

import mcio_ctrl as mcio
from mcio_ctrl.envs import mcio_env, minerl_env


def run() -> None:
    opts = mcio.types.RunOptions(mcio_mode=mcio.types.MCioMode.ASYNC)
    env = minerl_env.MinerlEnv(opts, render_mode="human")

    print("RESET")
    observation, info = env.reset(options={"commands": setup_commands})
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [99, 200]
    input("move curs >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["camera"] = [0, 0]
    action["inventory"] = 1
    input("e >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["inventory"] = 0
    input("release >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["camera"] = [0, 0.14]
    input("small move >")
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(action)
        env.render()

    action["camera"] = [0, 0]
    action["inventory"] = 1
    input("e close >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    env.close()


if __name__ == "__main__":
    mcio.util.logging_init()

    if len(sys.argv) != 2:
        print("Usage: python script.py <function_name>")
        print(
            "Available commands:",
            ", ".join(
                fn
                for fn in globals()
                if callable(globals()[fn]) and not fn.startswith("_")
            ),
        )
        sys.exit(1)

    cmd = sys.argv[1]
    fn = globals().get(cmd)
    if not callable(fn):
        print(f"No such command: {cmd}")
        sys.exit(1)

    fn()
