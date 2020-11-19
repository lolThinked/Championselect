var timerBox = document.querySelector(".timer");
var timerBlueDiv = document.querySelector("#timerBlue");
var timerRedDiv = document.querySelector("#timerRed");
var timerBlueText = document.querySelector("#timerBlue > h2");
var timerRedText = document.querySelector("#timerRed > h2");



var hoverDiv = document.querySelectorAll("div.player > div#hover");
//ChampionPick
var championBilder = document.querySelectorAll("div.player > div.champion > img");
//SummonerNames
var summonerNamesAll = document.querySelectorAll("div.player > div.SummonerName > h2");

//Summoners
var summonerSpellsDiv = document.querySelectorAll("div.player > div.champion > div.summonerSpellsR, div.player > div.champion > div.summonerSpells");
var summonerBilder1 = document.querySelectorAll("div.player > div.champion > div.summonerSpellsR >img#summonerSpell1, div.player > div.champion > div.summonerSpells >img#summonerSpell1");
var summonerBilder2 = document.querySelectorAll("div.player > div.champion > div.summonerSpellsR >img#summonerSpell2, div.player > div.champion > div.summonerSpells >img#summonerSpell2");
//Bans
var blueBans = document.querySelectorAll("div#blueTeamBans > div.ban > img");
var redBans = document.querySelectorAll("div#redTeamBans > div.ban > img");
//BAN-Text
var blueBansText = document.querySelectorAll("div#blueTeamBans > div.ban > div.Bantext >h1");
var blueBanDiv = document.querySelectorAll("div#blueTeamBans > div.ban > div.Bantext");
var redBansText = document.querySelectorAll("div#redTeamBans > div.ban > div.Bantext >h1");
var redBanDiv = document.querySelectorAll("div#redTeamBans > div.ban > div.Bantext");

var phaseDiv = document.getElementById("phase");

let delaytid = 180000;
delaytid = 10000;
//delaytid = 210000; //3min 30sek
delaytid = 180000; //3min
//delaytid = 5000;
//console.log("INFO");

function getInfo() {
    //console.log("HenterInfo");
    var xhr = new XMLHttpRequest();
    console.log(window.location.href);
    xhr.open('GET', window.location.href + "/json", true);
    xhr.send();
    //xhr.onreadystatechange = processRequest;
    xhr.onreadystatechange = setTimeout(() => {  processRequest(1); }, delaytid);
    //setTimeout(() => {  processRequest(1); }, delaytid);
    function processRequest(e) {
        	console.log(xhr.readyState + " : " + xhr.status)
var response = JSON.parse(xhr.responseText);
	console.log(response);
        if (xhr.readyState == 4 && xhr.status == 200 ) {

            var response = JSON.parse(xhr.responseText);
            for (var i = 0; i < 5; i++) {
                //PER PLAYER
                //BLUESIDE Check
                if (response.team.myTeam[i] != undefined) {
                  console.log("NOT UNDEFINED BLUESIDE");
                    //ChampionPick
                    if (response.team.myTeam[i].Pick != "None") {

                        championBilder[i].src = "static/pick/"+response.team.myTeam[i].Pick + ".png";

                    }
                    //Hovering
                    if (response.team.myTeam[i].Hover == false) {
                        hoverDiv[i].innerHTML = "<h2 style ='text-shadow: black -1px 0px, black 0px 1px, black 1px 0px, black 0px -1px;'>" + response.action.pickType + "</h2>";
                        hoverDiv[i].className = "Hovering";

                    } else if (response.team.myTeam[i].Hover == "Picking Next") {
                        hoverDiv[i].innerHTML = "<h3>Picking Next</h3>";
                        hoverDiv[i].className = "Hovering";

                    } else {
                        hoverDiv[i].className = "noneHover";
                    }
                    //Summoners
                    if (response.team.myTeam[i].SummonerSpell1 == undefined || response.team.myTeam[i].SummonerSpell1 == "None") {
                        summonerBilder1[i].style = "visibility:hidden;";
                        summonerBilder2[i].style = "visibility:hidden;";
                        summonerSpellsDiv[i].style = "visibility:hidden;";
                    } else if (response.team.myTeam[i].Pick != "None") {
                        //console.log("RESPONSE != ALT");

                        summonerBilder1[i].src = "static/spell/" + response.team.myTeam[i].SummonerSpell1 + ".png";
                        summonerBilder1[i].style = "";
                        summonerBilder2[i].src = "static/spell/" + response.team.myTeam[i].SummonerSpell2 + ".png";
                        summonerBilder2[i].style = "visibility:none;";
                        summonerSpellsDiv[i].style = "";
                    } else if (response.team.myTeam[i].Pick == "None") {
                        summonerBilder1[i].style = "visibility:hidden;";
                        summonerBilder2[i].style = "visibility:hidden;";
                        summonerSpellsDiv[i].style = "visibility:hidden;";
                    }
                } else {

                    championBilder[i].src = "static/nonePick.png";
                    summonerBilder1[i].style = "visibility:hidden;";
                    summonerBilder2[i].style = "visibility:hidden;";
                    summonerSpellsDiv[i].style = "visibility:hidden;";
                }
                //BLUESIDE Check END
                //REDSIDE Check
                if (response.team.theirTeam[i] != undefined) {
                  console.log("NOT UNDEFINED REDSIDE");
                    //ChampionPick
                    if (response.team.theirTeam[i].Pick != "None") {
                        championBilder[i + 5].src = "static/pick/" + response.team.theirTeam[i].Pick + ".png";
                        championBilder[i + 5].style = "-webkit-transform: scaleX(-1);";


                    }
                    //Hovering
                    if (response.team.theirTeam[i].Hover == false) {
                        //console.log("Picking");
                        hoverDiv[i + 5].innerHTML = "<h2 style ='text-shadow: black -1px 0px, black 0px 1px, black 1px 0px, black 0px -1px;'>" + response.action.pickType + "</h2>";
                        hoverDiv[i + 5].className = "HoveringRight";
                    } else if (response.team.theirTeam[i].Hover == "Picking Next") {
                        //console.log("Picking Next");
                        hoverDiv[i + 5].innerHTML = "<h3>" + response.team.theirTeam[i].Hover + "</h3>";
                        hoverDiv[i + 5].className = "HoveringRight";
                    } else {
                        //console.log("NONEHOVER");
                        hoverDiv[i + 5].className = "noneHover";
                    }
                    //Summoners
                    if (response.team.theirTeam[i].SummonerSpell1 == undefined || response.team.theirTeam[i].SummonerSpell1 == "None") {
                        summonerBilder1[i + 5].style = "visibility:hidden;";
                        summonerBilder2[i + 5].style = "visibility:hidden;";
                        summonerSpellsDiv[i+5].style = "visibility:hidden;";
                    } else if (response.team.theirTeam[i].SummonerSpell1 == "None") {
                        summonerBilder1[i + 5].style = "visibility:hidden;";
                        summonerBilder2[i + 5].style = "visibility:hidden;";
                        summonerSpellsDiv[i+5].style = "visibility:hidden;";
                    } else if (response.team.theirTeam[i].Pick != "None") {
                        //console.log("not None R");
                        summonerBilder1[i + 5].src = "static/spell/" + response.team.theirTeam[i].SummonerSpell1 + ".png";
                        summonerBilder1[i + 5].style = "";
                        summonerBilder2[i + 5].src = "static/spell/" + response.team.theirTeam[i].SummonerSpell2 + ".png";
                        summonerBilder2[i + 5].style = "visibility:none;";
                        summonerSpellsDiv[i+5].style = "";
                    } else if (response.team.theirTeam[i].Pick == "None") {
                        summonerBilder1[i + 5].style = "visibility:hidden;";
                        summonerBilder2[i + 5].style = "visibility:hidden;";
                        summonerSpellsDiv[i+5].style = "visibility:hidden;";
                    }
                } else {

                    championBilder[i + 5].src = "static/nonePick2.png";
                    championBilder[i + 5].style = "";
                    summonerBilder1[i + 5].style = "visibility:hidden;";
                    summonerBilder2[i + 5].style = "visibility:hidden;";
                    summonerSpellsDiv[i+5].style = "visibility:hidden;";

                }
                //REDSIDE Check END

                //BANS
                if (response.bans.myTeamBans[i] != "None") {
                    blueBans[i].src = "static/ban/" + response.bans.myTeamBans[i] + ".png";

                } else if (response.bans.myTeamBans[i] == "None") {

                    blueBans[i].src = "static/tall/" + (i + 1) + ".png";
                }
                if (response.bans.theirTeamBans[i] != "None") {
                    //console.log("BAN THEIR TEAM, i: " + (4-i));
                    redBans[4 - i].src = "static/ban/" + response.bans.theirTeamBans[i] + ".png";
                } else if (response.bans.theirTeamBans[i] == "None") {

                    redBans[4 - i].src = "static/tall/R" + (i + 1) + ".png";
                }
                //BANS END



            }
            if (response.action.pickType != undefined) {
                phaseDiv.innerHTML = "<h1 >" + (response.action.pickType).toUpperCase() + "</h1>";
            }

            //TIMER
            if (response.action.position > 4) {
                if(response.action.id == 20 || response.action.completed){//Both red and blueside timer shown
                  timerRedDiv.style = "visibility: visible;";
                  timerBlueDiv.style = "visibility:visible;";
                }else{
                  timerRedDiv.style = "visibility: visible;";
                  timerBlueDiv.style = "visibility:hidden;";
                }
                //phaseDiv.className = "phaseRed";
                //timerBox.id = "timerRed";
            } else {
                //phaseDiv.className = "phase";
                //timerBox.id = "timerBlue";
                timerRedDiv.style = "visibility: hidden;";
                timerBlueDiv.style = "visibility:visible;";
            }



        }
    }
}
function getTimer() {
    //console.log("HenterTimer");
    var xhr = new XMLHttpRequest();
    xhr.open('GET', window.location.href + "/timer", true);
    xhr.send();
    //xhr.onreadystatechange = processRequest;
    //xhr.onreadystatechange = setTimeout(() => {  processRequest; }, delaytid);
    xhr.onreadystatechange = setTimeout(() => {  processRequest(1); }, delaytid);
    //setTimeout(() => {  processRequest(1); }, delaytid);
    function processRequest(e) {
        //console.log(xhr.readyState)
        if (xhr.readyState == 4 && xhr.status == 200) {
            // time to partay!!!
            var response = JSON.parse(xhr.responseText);
            //console.log("response.timer = "+response.time);
            //timerBox.innerHTML = "<h1 style='margin-top: -3px; margin-left: -40px;'>:" + response.time + "</h1>";
            //console.log(timerBox.innerHTML);
            timerRedText.innerHTML = response.time;
            timerBlueText.innerHTML = response.time;
        }
    }


}
function setNames() {
    //console.log("GettingNamesJson");
    var xhr = new XMLHttpRequest();
    xhr.open('GET', window.location.href+"/json", true);
    xhr.send();
    //xhr.onreadystatechange = processRequest;
    //setTimeout(() => {  processRequest(1); }, delaytid);
    xhr.onreadystatechange = setTimeout(() => {  processRequest(1); }, delaytid);
    function processRequest(e) {
        //	console.log(xhr.readyState)
        if (xhr.readyState == 4 && xhr.status == 200) {
            // time to partay!!!
            var response = JSON.parse(xhr.responseText);
            for (var i = 0; i < 5; i++) {
                //BLUESIDE
                if (response.team.myTeam[i] == undefined) {
                    summonerNamesAll[i].innerHTML = "";
                    summonerNamesAll[i].style = "text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;";
                } else {
                    summonerNamesAll[i].innerHTML = response.team.myTeam[i].Name + " ";
                    summonerNamesAll[i].style = "text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;";
                    //summonerNamesAll[4-i].style = "font-size:0.1vw";
                    //summonerNamesAll[4-i].style = "font-size:" + (50-(response.team.myTeam[i].Name).length)*0.030 + "vw; margin-top: 0px;";
                    //summonerNamesAll[i].style = "position: absolute; right: 33px; top: 38px;";
                }
                //REDSIDE
                if (response.team.theirTeam[i] == undefined) {
                    summonerNamesAll[i + 5].innerHTML = "";
                    summonerNamesAll[i + 5].style = "text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;";
                } else {
                    summonerNamesAll[i + 5].innerHTML = response.team.theirTeam[i].Name;
                    summonerNamesAll[i + 5].style = "text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;";
                    //summonerNamesAll[i+5].style = "font-size:" + (25-(response.team.theirTeam[i].Name).length)*0.09 + "vw; margin-top: 0px;";
                    //summonerNamesAll[i+5].style = "postition: absolute; left: 10px; top: 38px; position: absolute;";

                }
                //BANS CSS
                //blueBansText[i].innerHTML = "Ban "+(i+1);
                //blueBanDiv[i].style = " position: relative; top:-134px;    background-color: #0000008c; border-radius: 16px;";
                //redBansText[i].innerHTML = "Ban "+(5-i);
                //redBanDiv[i].style = " position: relative; top:-134px;    background-color: #0000008c; border-radius: 16px;";


            }
        }
    }


}
document.onkeydown = checkKey;
function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '190') {
        setNames();
        // up arrow
    }

}
function timer(ms) {
    return new Promise(res => setTimeout(res, ms));
}
//setInterval(getInfo(), 500);
//getInfo();
var teller = 0;
async function load() {
    await timer(1500);
    while (true) {
        if (teller == 4) {
        //console.log("GET Timer");
	    await getTimer();
	//console.log("GET INFO");
            await getInfo();
	//console.log("GET Names");
            await setNames();
            teller = 0;
        } else {
            await getTimer();
            teller++;
        }


        await timer(250);
    }
}
setNames();
getTimer();
getInfo();


load();
