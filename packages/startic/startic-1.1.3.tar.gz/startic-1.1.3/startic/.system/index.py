from imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args
        # ...
        cli.dev = "-dev" in args
        self.started = False
        self.config = self.cwd + "/assets/startic.json"
        self.pages = self.cwd + "/pages.yml"
        self.configs = {}
        pass

    def __exit__(self):
        # ...
        pass

    ####################################################################################// Main
    def new(self, cmd=""):  # Create new project
        if cli.isFile(self.config):
            return "Project already exists!"

        frame = self.app + "/frame"
        if not cli.isFolder(frame):
            return "Invalid frame!"

        shutil.copytree(frame, self.cwd, dirs_exist_ok=True)

        return "Project created successfully"

    def start(self, cmd=""):  # Start project development
        if not cli.isFile(self.config):
            return "Project does not exist!"

        if not cli.isFile(self.pages):
            return "Invalid pages map!"

        print("Press Ctrl+C to stop")
        self.__open()

        hint = "..."
        self.started = True
        originID = self.__changeID(self.cwd)

        while True:
            hint = ".." if hint == "." else ("..." if hint == ".." else ".")
            if originID != self.__changeID(self.cwd):
                hint = "rendering ..."
                self.render()
                originID = self.__changeID(self.cwd)

            cli.done("Watching for changes: " + hint, True)
            time.sleep(2)
        pass

    def render(self, update="", cmd=""):  # Render project pages
        if not cli.isFile(self.config):
            return "Project does not exist!"

        self.configs = {}
        yaml = cli.yaml(self.pages)
        if not yaml:
            cli.error("Invalid page map")
            return False

        file = f"{self.cwd}/parts/.html"
        frame = cli.read(file).replace("((...))", "{({...})}").strip()
        if not frame:
            cli.trace("Invalid page frame")
            return False

        shape = self.__renderSection(frame).strip()
        for page in yaml:
            self.__renderPage(shape, page, yaml)

        sitemap = self.app + "/.system/sources/sitemap.xml"
        configured = self.__renderConfig(cli.read(sitemap))
        parsed = self.__parseSystemVars(configured)
        cli.write(self.cwd + "/assets/sitemap.xml", parsed)

        if update != "-u":
            self.__open()

        return "Project rendered successfully"

    ####################################################################################// Helpers
    def __renderPage(self, frame: str, page: str, yaml: dict):
        html = ""
        for section in yaml[page]:
            path = section.replace(" - ", "/").strip()
            file = f"{self.cwd}/{path}.html"
            if not cli.isFile(file):
                continue
            read = (
                f"\n<!-- {section} - start -->\n"
                + cli.read(file)
                + f"\n<!-- {section} - end -->\n"
            )
            cased = self.__renderFeedCases(read)
            feeded = self.__renderFeeders(cased)
            html += self.__renderSection(feeded).strip()
            cli.trace(f"Rendered section: {page}({path})")

        content = frame.replace(
            "{({...})}",
            "\n<!-- frame - start -->\n" + html + "\n<!-- frame - end -->\n",
        )
        pagedir = f"{self.cwd}/{page}"
        if page == "index":
            pagedir = self.cwd

        configured = self.__renderConfig(content)
        parsed = self.__parseSystemVars(configured)
        os.makedirs(pagedir, exist_ok=True)
        cli.write(f"{pagedir}/index.html", parsed)

        return True

    def __renderSection(self, content: str):
        matches = re.findall(r"\(\((.*?)\)\)", content)
        if not matches:
            return content

        done = []
        parsed = False
        for hint in matches:
            item = hint.replace(": ", "/")
            file = f"{self.cwd}/{item}.html"
            if not cli.isFile(file):
                content = content.replace("((" + hint + "))", "")
                continue
            if hint != "..." and hint not in done:
                html = cli.read(file).replace("((" + hint + "))", "")
                content = content.replace(
                    "((" + hint + "))",
                    f"\n<!-- {hint} - start -->\n"
                    + html
                    + f"\n<!-- {hint} - end -->\n",
                )
                done.append(hint)
                parsed = True

        return self.__renderSection(content) if parsed else content

    def __renderFeeders(self, content: str):
        matches = re.findall(r"\[\[(.*?)\]\]", content)
        if not matches:
            return content

        for item in matches:
            rvs = "!" if item[0] == "!" else ""
            if rvs:
                item = item[1:]

            path = f"{self.cwd}/{item}"
            if not cli.isFolder(path):
                continue

            html = ""
            cli.trace("Rendering feeder: " + item)
            files = os.listdir(path)
            if rvs:
                files.reverse()
            for file in files:
                if file == "index.html":
                    continue
                html += cli.read(f"{path}/{file}").replace("[[" + rvs + item + "]]", "")
            content = content.replace(
                "[[" + rvs + item + "]]",
                f"\n<!-- {item} feeder - start -->\n"
                + html
                + f"\n<!-- {item} feeder - end -->\n",
            )

        return self.__renderFeeders(content)

    def __renderFeedCases(self, content: str):
        matches = re.findall(r"\[\[(.*?): (.*?)\]\]", content)
        if not matches:
            return content

        for folder, case in matches:
            path = f"{self.cwd}/{folder}"
            if not cli.isFolder(path):
                content = content.replace(f"[[{folder}: {case}]]", "")
                continue

            files = os.listdir(path)
            if not files:
                content = content.replace(f"[[{folder}: {case}]]", "")
                continue

            if "index.html" in files:
                files.remove("index.html")

            html = ""
            if case == "first":
                html = cli.read(path + "/" + files[0])
            elif case == "count":
                html = str(len(files))
            elif case == "last":
                html = cli.read(path + "/" + files[-1])

            cli.trace(f"Rendering feed case: {folder}.{case}")
            content = content.replace(
                f"[[{folder}: {case}]]",
                f"\n<!-- {folder} feed case {case} - start -->\n"
                + html
                + f"\n<!-- {folder} feed case {case} - end -->\n",
            )

        return self.__renderFeedCases(content)

    def __renderConfig(self, content: str):
        matches = re.findall(r"\{\{(.*?)\}\}", content)
        if not matches:
            return content

        for item in matches:
            parts = item.split(": ")
            name = cli.value(0, parts).strip()
            config = f"{self.cwd}/assets/{name}.json"
            key = cli.value(1, parts).strip()
            if not name or not cli.isFile(config) or not key:
                continue
            if name not in self.configs:
                cli.trace("Reading config: " + name)
                self.configs[name] = json.loads(cli.read(config))

            value = cli.value(key, self.configs[name])
            content = content.replace("{{" + item + "}}", value)

        return self.__renderFeeders(content)

    def __parseSystemVars(self, content: str):
        Vars = self.__vars()
        for var in Vars:
            content = content.replace("{{" + var + "}}", Vars[var])
        return content

    def __changeID(self, folder: str):
        collect = ""
        for root, dirs, files in os.walk(folder):
            for name in dirs + files:
                full_path = os.path.join(root, name)
                mtime = os.path.getmtime(full_path)
                readable_time = datetime.fromtimestamp(mtime)
                collect += full_path + str(readable_time)
        return collect

    def __open(self):
        index = f"{self.cwd}/index.html"
        if self.started or not cli.isFile(index):
            return False

        cli.trace("Opening index file ...")
        webbrowser.open(f"file://{index}")

        return False

    def __vars(self):
        return {
            "DATE": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            # "": "",
        }
