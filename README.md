<div align="center">

<img src="assets/hero.svg" alt="Arjun Nair: I build race-engineering software from raw telemetry" width="100%">

</div>

I like problems where the data arrives live and the answer has to be right. Most of what I build turns raw Formula 1 telemetry into decisions: who undercuts whom, which corner cost you the lap, whether a different pit stop would have won the race. I work end to end, from UDP packets and timing feeds through Python models to apps on the web, iOS, Android and Windows. And I test it until I trust it.

<img src="assets/kerb.svg" width="100%" height="14" alt="">

## The garage

<table>
<tr>
<td width="50%" valign="top">

### [Pit Wall](https://github.com/arjun-nair1090/Pitwall)
<a href="https://github.com/arjun-nair1090/Pitwall"><img src="https://raw.githubusercontent.com/arjun-nair1090/Pitwall/HEAD/docs/readme/live.svg" alt="Pit Wall live timing" width="100%"></a>

Live F1 timing plus a replay of every race since 2018: telemetry head-to-heads, a strategy simulator, lap-by-lap win probability and Monte Carlo title odds. A language model only writes sentences around numbers the code computed, and those sentences are checked before they're shown.

`Next.js` `FastAPI` `PostgreSQL` `Redis` `WebSockets` `Docker` · **1,618 tests**

</td>
<td width="50%" valign="top">

### [PurpleSector](https://github.com/arjun-nair1090/purplesector)
<a href="https://github.com/arjun-nair1090/purplesector"><img src="https://raw.githubusercontent.com/arjun-nair1090/purplesector/HEAD/docs/screenshots/live.png" alt="PurpleSector live dashboard" width="100%"></a>

A pit wall on your second monitor and a race engineer in your headset, for F1 22 to F1 25. It lines up every lap metre by metre, tells you which corner cost you time before you reach the next one, and only speaks when the data backs it up. Fully offline; ships as a single Windows exe.

`Python` `UDP telemetry` `Streamlit` `TTS` · **[v1.1.0 released](https://github.com/arjun-nair1090/purplesector/releases)**

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [APEX](https://github.com/arjun-nair1090/apex-f1-widgets)
<a href="https://github.com/arjun-nair1090/apex-f1-widgets"><img src="https://raw.githubusercontent.com/arjun-nair1090/apex-f1-widgets/HEAD/docs/readme/hero.svg" alt="APEX F1 widgets" width="100%"></a>

Ten home-screen widgets that count down to lights out, switch to live timing on their own, then to results. Native on three platforms, fed by one FastAPI live-timing server.

`Swift` `Kotlin` `C#` `FastAPI` · **iOS · Android · Windows**

</td>
<td width="50%" valign="top">

### [FitRank](https://github.com/arjun-nair1090/FitRankPro)
<a href="https://arjun-nair1090.github.io/FitRankPro/"><img src="https://raw.githubusercontent.com/arjun-nair1090/FitRankPro/HEAD/docs/screenshots/progress-desktop.png" alt="FitRank progress charts" width="100%"></a>

A workout tracker with a Java API on PostgreSQL: a fast set logger, PR detection by estimated 1RM, and Hevy and Apple Health imports streamed in the browser so huge exports still work.

`Java` `PostgreSQL` `JavaScript` · **[try the live demo](https://arjun-nair1090.github.io/FitRankPro/)**

</td>
</tr>
</table>

**Also on the grid:** [Resonance](https://github.com/arjun-nair1090/Resonance), a music platform with a hybrid recommender (content, collaborative and behaviour signals) on Next.js, FastAPI, Postgres and Redis · [TradeBot](https://github.com/arjun-nair1090/TradeBot), a Binance Futures CLI with hand-rolled HMAC-SHA256 request signing.

<img src="assets/kerb.svg" width="100%" height="14" alt="">

## How I build

- **Numbers come from code.** Models, probabilities and strategy calls are computed in plain, tested Python. AI writes the words, never the facts.
- **Tested until it's boring.** Pit Wall's backend has over 1,600 tests, and CI runs them on every pull request.
- **Ship it.** Real releases, live demos and one-command setup: `docker compose up`, or unzip and run.
- **Same product, every screen.** One backend feeding web, iOS, Android and Windows clients.

## Toolbox

<p>
<img src="https://skillicons.dev/icons?i=python,ts,js,java,swift,kotlin,cs&theme=dark" alt="Languages">
<br>
<img src="https://skillicons.dev/icons?i=fastapi,nextjs,react,tailwind,postgres,redis,docker,githubactions&theme=dark" alt="Frameworks and infrastructure">
</p>

<div align="center">
<br>
<sub>Built in Mumbai · open to software engineering roles</sub>
</div>
