from pathlib import Path

from framework.configuration.config_loader import ConfigLoader


def main():

    project_root = Path(__file__).resolve().parent.parent

    loader = ConfigLoader(project_root)

    config = loader.load(
        environment="dev",
        dataset="green_tripdata"
    )

    print(config)


if __name__ == "__main__":
    main()
