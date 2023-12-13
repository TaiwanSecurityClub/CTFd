import Alpine from "alpinejs";
import CTFd from "./index";
import { getOption } from "./utils/graphs/echarts/scoreboard";
import { embed } from "./utils/graphs/echarts";

window.Alpine = Alpine;
window.CTFd = CTFd;

Alpine.data("ScoreboardDetail", () => ({
  data: null,

  async init() {
    const response = await CTFd.fetch(`/api/v1/scoreboard/top/10?qualify`, {
      method: "GET",
    });
    const body = await response.json();
    this.data =  body["data"]; // scoreboard data

    let option = getOption(CTFd.config.userMode, this.data);
    embed(this.$refs.scoregraph, option);
  },
}));

Alpine.start();
