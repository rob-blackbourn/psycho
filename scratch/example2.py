from packaging.requirements import Requirement


def main() -> None:
    req = Requirement("proj1 @ ../proj1")
    print(f"Requirement name: {req.name}")


if __name__ == "__main__":
    main()
