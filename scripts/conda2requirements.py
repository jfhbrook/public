import yaml

with open("./environment.yml", "r") as f:
    environment_yml = yaml.safe_load(f)

requirements = []

for dependency in environment_yml["dependencies"]:
    if any([blacklisted_module in dependency for blacklisted_module in {"python"}]):
        continue

    if type(dependency) == dict and "pip" in dependency:
        requirements += dependency["pip"]
    else:
        tokens = dependency.split("=")
        if len(tokens) == 1:
            module = tokens[0]
            version = None
        elif len(tokens) == 2:
            module, version = tokens
            if "*" in version:
                print(
                    f"WARNING: version `{version}` incompatible with pip; "
                    "not setting version"
                )
                version = None
        else:
            raise Exception(f"Don't know what to do with {dependency}")
        if version:
            requirements.append(f"{module}=={version}")
        else:
            requirements.append(module)

requirements.sort()

with open("./requirements.in", "w") as f:
    f.write("\n".join(requirements))
