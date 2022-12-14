from fastapi import FastAPI
import pandas as pd
import numpy as np
import datetime
import requests
import pickle
import sklearn
import os

app = FastAPI()
print(os.listdir(os.getcwd()))

with open("./model.pkl", "rb") as f:
  model = pickle.load(f)


@app.get("/")
def read_root():
  return {"Hello": "Test"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/odds")
def get_todays_odds():
  today = datetime.date.today()
  API_KEY = '37729deaa25e0db55528466df78c130e'
  SPORT = 'basketball_ncaab' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
  REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
  MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
  ODDS_FORMAT = 'american' # decimal | american
  DATE_FORMAT = 'unix' # iso | unix
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #
  # First get a list of in-season sports
  #   The sport 'key' from the response can be used to get odds in the next request
  #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  sports_response = requests.get(
      'https://api.the-odds-api.com/v4/sports',
      params={
          'api_key': API_KEY
      }
  )

  if sports_response.status_code != 200:
      print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

  else:
      print('List of in season sports:', sports_response.json())

   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #
  # Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
  # This will deduct from the usage quota
  # The usage quota cost = [number of markets specified] x [number of regions specified]
  # For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
  #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  odds_response = requests.get(
      f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
      params={
          'api_key': API_KEY,
          'regions': REGIONS,
          'markets': MARKETS,
          'oddsFormat': ODDS_FORMAT,
          'dateFormat': DATE_FORMAT,
      }
  )

  if odds_response.status_code != 200:
      print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

  else:
      odds_json = odds_response.json()

  df_alt_names = []
  df_alt_names.append(["Alabama Crimson Tide", "Alabama"])
  df_alt_names.append(["Vanderbilt Commodores", "Vanderbilt"])
  df_alt_names.append(["San Diego St Aztecs", "San Diego State"])
  df_alt_names.append(["Boise State Broncos", "Boise State"])
  df_alt_names.append(["New Mexico Lobos", "New Mexico"])
  df_alt_names.append(["Utah State Aggies", "Utah State"])
  df_alt_names.append(["UNLV Rebels", "UNLV"])
  df_alt_names.append(["Nevada Wolf Pack", "Nevada"])
  df_alt_names.append(["Bucknell Bison", "Bucknell"])
  df_alt_names.append(["Army Knights", "Army"])
  df_alt_names.append(["Creighton Bluejays", "Creighton"])
  df_alt_names.append(["St. John's Red Storm", "St. John's"])
  df_alt_names.append(["Mississippi St Bulldogs", "Mississippi State"])
  df_alt_names.append(["South Carolina Gamecocks", "South Carolina"])
  df_alt_names.append(["Boston College Eagles", "Boston College"])
  df_alt_names.append(["NC State Wolfpack", "NC State"])
  df_alt_names.append(["Chattanooga Mocs", "Chattanooga"])
  df_alt_names.append(["East Tennessee St Buccaneers", "East Tennessee State"])
  df_alt_names.append(["Wake Forest Demon Deacons", "Wake Forest"])
  df_alt_names.append(["Clemson Tigers", "Clemson"])
  df_alt_names.append(["Davidson Wildcats", "Davidson"])
  df_alt_names.append(["Duquesne Dukes", "Duquesne"])
  df_alt_names.append(["Drake Bulldogs", "Drake"])
  df_alt_names.append(["Valparaiso Crusaders", "Valparaiso"])
  df_alt_names.append(["Duke Blue Devils", "Duke"])
  df_alt_names.append(["Virginia Cavaliers", "Virginia"])
  df_alt_names.append(["South Florida Bulls", "South Florida"])
  df_alt_names.append(["East Carolina Pirates", "East Carolina"])
  df_alt_names.append(["La Salle Explorers", "La Salle"])
  df_alt_names.append(["Fordham Rams", "Fordham"])
  df_alt_names.append(["George Mason Patriots", "George Mason"])
  df_alt_names.append(["VCU Rams", "VCU"])
  df_alt_names.append(["Louisiana Ragin' Cajuns", "Lafayette"])
  df_alt_names.append(["Georgia Southern Eagles", "Georgia Southern"])
  df_alt_names.append(["UL Monroe Warhawks", "UL Monroe"])
  df_alt_names.append(["Georgia St Panthers", "Georgia State"])
  df_alt_names.append(["Northern Iowa Panthers", "Northern Iowa"])
  df_alt_names.append(["Indiana St Sycamores", "Indiana State"])
  df_alt_names.append(["West Virginia Mountaineers", "West Virginia"])
  df_alt_names.append(["Iowa State Cyclones", "Iowa State"])
  df_alt_names.append(["James Madison Dukes", "James Madison"])
  df_alt_names.append(["Towson Tigers", "Towson"])
  df_alt_names.append(["The Citadel Bulldogs", "The Citadel"])
  df_alt_names.append(["Mercer Bears", "Mercer"])
  df_alt_names.append(["Syracuse Orange", "Syracuse"])
  df_alt_names.append(["Notre Dame Fighting Irish", "Notre Dame"])
  df_alt_names.append(["Xavier Musketeers", "Xavier"])
  df_alt_names.append(["Providence Friars", "Providence"])
  df_alt_names.append(["Texas Longhorns", "Texas"])
  df_alt_names.append(["TCU Horned Frogs", "TCU"])
  df_alt_names.append(["UT-Arlington Mavericks", "UT Arlington"])
  df_alt_names.append(["Troy Trojans", "Troy"])
  df_alt_names.append(["Western Carolina Catamounts", "Western Carolina"])
  df_alt_names.append(["UNC Greensboro Spartans", "UNC Greensboro"])
  df_alt_names.append(["Wofford Terriers", "Wofford"])
  df_alt_names.append(["VMI Keydets", "VMI"])
  df_alt_names.append(["Appalachian St Mountaineers", "Appalachian State"])
  df_alt_names.append(["Arkansas-Little Rock Trojans", "Little Rock"])
  df_alt_names.append(["Coastal Carolina Chanticleers", "Coastal Carolina"])
  df_alt_names.append(["Arkansas St Red Wolves", "Arkansas State"])
  df_alt_names.append(["Bradley Braves", "Bradley"])
  df_alt_names.append(["Missouri St Bears", "Missouri State"])
  df_alt_names.append(["Grand Canyon Antelopes", "Grand Canyon"])
  df_alt_names.append(["Chicago St Cougars", "Chicago State"])
  df_alt_names.append(["Evansville Purple Aces", "Evansville"])
  df_alt_names.append(["Loyola (Chi) Ramblers", "Loyola Chicago"])
  df_alt_names.append(["Furman Paladins", "Furman"])
  df_alt_names.append(["Samford Bulldogs", "Samford"])
  df_alt_names.append(["Houston Cougars", "Houston"])
  df_alt_names.append(["Tulane Green Wave", "Tulane"])
  df_alt_names.append(["Illinois St Redbirds", "Illinois State"])
  df_alt_names.append(["Southern Illinois Salukis", "Southern Illinois"])
  df_alt_names.append(["Tulsa Golden Hurricane", "Tulsa"])
  df_alt_names.append(["SMU Mustangs", "SMU"])
  df_alt_names.append(["Texas State Bobcats", "Texas State"])
  df_alt_names.append(["South Alabama Jaguars", "South Alabama"])
  df_alt_names.append(["Ole Miss Rebels", "Ole Miss"])
  df_alt_names.append(["Auburn Tigers", "Auburn"])
  df_alt_names.append(["Cincinnati Bearcats", "Cincinnati"])
  df_alt_names.append(["UCF Knights", "UCF"])
  df_alt_names.append(["Wyoming Cowboys", "Wyoming"])
  df_alt_names.append(["Colorado St Rams", "Colorado State"])
  df_alt_names.append(["Virginia Tech Hokies", "Virginia Tech"])
  df_alt_names.append(["Georgia Tech Yellow Jackets", "Georgia Tech"])
  df_alt_names.append(["LSU Tigers", "LSU"])
  df_alt_names.append(["Kentucky Wildcats", "Kentucky"])
  df_alt_names.append(["Wisconsin Badgers", "Wisconsin"])
  df_alt_names.append(["Minnesota Golden Gophers", "Minnesota"])
  df_alt_names.append(["Washington Huskies", "Washington"])
  df_alt_names.append(["Washington St Cougars", "Washington State"])
  df_alt_names.append(["Albany Great Danes", "Albany"])
  df_alt_names.append(["Maine Black Bears", "Maine"])
  df_alt_names.append(["American Eagles", "American University"])
  df_alt_names.append(["Lehigh Mountain Hawks", "Lehigh"])
  df_alt_names.append(["Binghamton Bearcats", "Binghamton"])
  df_alt_names.append(["Lafayette Leopards", "Lafayette"])
  df_alt_names.append(["Boston Univ. Terriers", "Boston University"])
  df_alt_names.append(["Campbell Fighting Camels", "Campbell"])
  df_alt_names.append(["Hampton Pirates", "Hampton"])
  df_alt_names.append(["Central Arkansas Bears", "Central Arkansas"])
  df_alt_names.append(["North Alabama Lions", "North Alabama"])
  df_alt_names.append(["Charleston Southern Buccaneers", "Charleston Southern"])
  df_alt_names.append(["Presbyterian Blue Hose", "Presbyterian"])
  df_alt_names.append(["Eastern Kentucky Colonels", "Eastern Kentucky"])
  df_alt_names.append(["Jacksonville St Gamecocks", "Jacksonville State"])
  df_alt_names.append(["Florida Gulf Coast Eagles", "Florida Gulf Coast"])
  df_alt_names.append(["Liberty Flames", "Liberty"])
  df_alt_names.append(["Gardner-Webb Bulldogs", "Gardner-Webb"])
  df_alt_names.append(["UNC Asheville Bulldogs", "UNC Asheville"])
  df_alt_names.append(["North Florida Ospreys", "North Florida"])
  df_alt_names.append(["Jacksonville Dolphins", "Jacksonville"])
  df_alt_names.append(["UMBC Retrievers", "UMBC"])
  df_alt_names.append(["Hartford Hawks", "Hartford"])
  df_alt_names.append(["High Point Panthers", "High Point"])
  df_alt_names.append(["North Carolina A&T Aggies", "North Carolina A&T"])
  df_alt_names.append(["Stetson Hatters", "Stetson"])
  df_alt_names.append(["Kennesaw St Owls", "Kennesaw State"])
  df_alt_names.append(["Radford Highlanders", "Radford"])
  df_alt_names.append(["Longwood Lancers", "Longwood"])
  df_alt_names.append(["Loyola (MD) Greyhounds", "Loyola MD"])
  df_alt_names.append(["Navy Midshipmen", "Navy"])
  df_alt_names.append(["Stony Brook Seawolves", "Stony Brook"])
  df_alt_names.append(["UMass Lowell River Hawks", "UMass Lowell"])
  df_alt_names.append(["Colgate Raiders", "Colgate"])
  df_alt_names.append(["Holy Cross Crusaders", "Holy Cross"])
  df_alt_names.append(["Vermont Catamounts", "Vermont"])
  df_alt_names.append(["William & Mary Tribe", "William & Mary"])
  df_alt_names.append(["Northeastern Huskies", "Northeastern"])
  df_alt_names.append(["Bryant Bulldogs", "Bryant"])
  df_alt_names.append(["St. Francis BKN Terriers", "St. Francis BKN"])
  df_alt_names.append(["Central Connecticut St Blue Devils", "Central Connecticut"])
  df_alt_names.append(["St. Francis (PA) Red Flash", "St. Francis PA"])
  df_alt_names.append(["Central Michigan Chippewas", "Central Michigan"])
  df_alt_names.append(["Miami (OH) RedHawks", "Miami OH"])
  df_alt_names.append(["Charleston Cougars", "Charleston"])
  df_alt_names.append(["Delaware Blue Hens", "Delaware"])
  df_alt_names.append(["Charlotte 49ers", "Charlotte"])
  df_alt_names.append(["Florida Int'l Golden Panthers", "Florida International"])
  df_alt_names.append(["Cleveland St Vikings", "Cleveland State"])
  df_alt_names.append(["Detroit Mercy Titans", "Detroit Mercy"])
  df_alt_names.append(["UNC Wilmington Seahawks", "UNC Wilmington"])
  df_alt_names.append(["Drexel Dragons", "Drexel"])
  df_alt_names.append(["Hofstra Pride", "Hofstra"])
  df_alt_names.append(["Elon Phoenix", "Elon"])
  df_alt_names.append(["Florida Atlantic Owls", "Florida Atlantic"])
  df_alt_names.append(["Old Dominion Monarchs", "Old Dominion"])
  df_alt_names.append(["Fort Wayne Mastodons", "Purdue Fort Wayne"])
  df_alt_names.append(["Oakland Golden Grizzlies", "Oakland"])
  df_alt_names.append(["Maryland Terrapins", "Maryland"])
  df_alt_names.append(["Indiana Hoosiers", "Indiana"])
  df_alt_names.append(["Marshall Thundering Herd", "Marshall"])
  df_alt_names.append(["Middle Tennessee Blue Raiders", "Middle Tennessee"])
  df_alt_names.append(["Temple Owls", "Temple"])
  df_alt_names.append(["Memphis Tigers", "Memphis"])
  df_alt_names.append(["Mt. St. Mary's Mountaineers", "Mount St. Mary's"])
  df_alt_names.append(["Sacred Heart Pioneers", "Sacred Heart"])
  df_alt_names.append(["Robert Morris Colonials", "Robert Morris"])
  df_alt_names.append(["Northern Kentucky Norse", "Northern Kentucky"])
  df_alt_names.append(["Omaha Mavericks", "Omaha"])
  df_alt_names.append(["Western Illinois Leathernecks", "Western Illinois"])
  df_alt_names.append(["Siena Saints", "Siena"])
  df_alt_names.append(["Quinnipiac Bobcats", "Quinnipiac"])
  df_alt_names.append(["South Carolina Upstate Spartans", "South Carolina Upstate"])
  df_alt_names.append(["Winthrop Eagles", "Winthrop"])
  df_alt_names.append(["Youngstown St Penguins", "Youngstown State"])
  df_alt_names.append(["Wright St Raiders", "Wright State"])
  df_alt_names.append(["Sam Houston St Bearkats", "Sam Houston"])
  df_alt_names.append(["Stephen F. Austin Lumberjacks", "Stephen F. Austin"])
  df_alt_names.append(["Lamar Cardinals", "Lamar"])
  df_alt_names.append(["Abilene Christian Wildcats", "Abilene Christian"])
  df_alt_names.append(["Buffalo Bulls", "Buffalo"])
  df_alt_names.append(["Northern Illinois Huskies", "Northern Illinois"])
  df_alt_names.append(["DePaul Blue Demons", "DePaul"])
  df_alt_names.append(["Georgetown Hoyas", "Georgetown"])
  df_alt_names.append(["Eastern Washington Eagles", "Eastern Washington"])
  df_alt_names.append(["N Colorado Bears", "Northern Colorado"])
  df_alt_names.append(["Green Bay Phoenix", "Green Bay"])
  df_alt_names.append(["UIC Flames", "UIC"])
  df_alt_names.append(["Incarnate Word Cardinals", "Incarnate Word"])
  df_alt_names.append(["Houston Baptist Huskies", "Houston Baptist"])
  df_alt_names.append(["Milwaukee Panthers", "Milwaukee"])
  df_alt_names.append(["IUPUI Jaguars", "IUPUI"])
  df_alt_names.append(["Idaho State Bengals", "Idaho State"])
  df_alt_names.append(["Northern Arizona Lumberjacks", "Northern Arizona"])
  df_alt_names.append(["Louisiana Tech Bulldogs", "Louisiana Tech"])
  df_alt_names.append(["Rice Owls", "Rice"])
  df_alt_names.append(["Southern Miss Golden Eagles", "Southern Miss"])
  df_alt_names.append(["North Texas Mean Green", "North Texas"])
  df_alt_names.append(["South Dakota St Jackrabbits", "South Dakota State"])
  df_alt_names.append(["Oral Roberts Golden Eagles", "Oral Roberts"])
  df_alt_names.append(["Tenn-Martin Skyhawks", "UT Martin"])
  df_alt_names.append(["SE Missouri St Redhawks", "Southeast Missouri State"])
  df_alt_names.append(["Seattle Redhawks", "Seattle U"])
  df_alt_names.append(["Utah Valley Wolverines", "Utah Valley"])
  df_alt_names.append(["South Dakota Coyotes", "South Dakota"])
  df_alt_names.append(["UMKC Kangaroos", "Kansas City"])
  df_alt_names.append(["UAB Blazers", "UAB"])
  df_alt_names.append(["UTSA Roadrunners", "UTSA"])
  df_alt_names.append(["Austin Peay Governors", "Austin Peay"])
  df_alt_names.append(["SIU-Edwardsville Cougars", "SIU Edwardsville"])
  df_alt_names.append(["Morehead St Eagles", "Morehead State"])
  df_alt_names.append(["Eastern Illinois Panthers", "Eastern Illinois"])
  df_alt_names.append(["Texas A&M-CC Islanders", "Texas A&M-CC"])
  df_alt_names.append(["Mcneese St Mcneese", "McNeese"])
  df_alt_names.append(["Nicholls St Colonels", "Nicholls"])
  df_alt_names.append(["Northwestern St Demons", "Northwestern State"])
  df_alt_names.append(["Tennessee St Tigers", "Tennessee State"])
  df_alt_names.append(["Tennessee Tech Golden Eagles", "Tennessee Tech"])
  df_alt_names.append(["Arizona St Sun Devils", "Arizona State"])
  df_alt_names.append(["Colorado Buffaloes", "Colorado"])
  df_alt_names.append(["Belmont Bruins", "Belmont"])
  df_alt_names.append(["Murray St Racers", "Murray State"])
  df_alt_names.append(["Cal Baptist Lancers", "California Baptist"])
  df_alt_names.append(["Dixie State Trailblazers", "Dixie State"])
  df_alt_names.append(["Gonzaga Bulldogs", "Gonzaga"])
  df_alt_names.append(["San Francisco Dons", "San Francisco"])
  df_alt_names.append(["Ohio State Buckeyes", "Ohio State"])
  df_alt_names.append(["Illinois Fighting Illini", "Illinois"])
  df_alt_names.append(["Montana Grizzlies", "Montana"])
  df_alt_names.append(["Southern Utah Thunderbirds", "Southern Utah"])
  df_alt_names.append(["New Orleans Privateers", "New Orleans"])
  df_alt_names.append(["SE Louisiana Lions", "SE Louisiana"])
  df_alt_names.append(["UC Santa Barbara Gauchos", "UC Santa Barbara"])
  df_alt_names.append(["UC Davis Aggies", "UC Davis"])
  df_alt_names.append(["UCLA Bruins", "UCLA"])
  df_alt_names.append(["Oregon Ducks", "Oregon"])
  df_alt_names.append(["Loyola Marymount Lions", "Loyola Marymount"])
  df_alt_names.append(["BYU Cougars", "BYU"])
  df_alt_names.append(["UC Irvine Anteaters", "UC Irvine"])
  df_alt_names.append(["CSU Fullerton Titans", "CSU Fullerton"])
  df_alt_names.append(["CSU Northridge Matadors", "CSU Northridge"])
  df_alt_names.append(["UC Riverside Highlanders", "UC Riverside"])
  df_alt_names.append(["Idaho Vandals", "Idaho"])
  df_alt_names.append(["Sacramento St Hornets", "Sacramento State"])
  df_alt_names.append(["UC San Diego Tritons", "UC San Diego"])
  df_alt_names.append(["Long Beach St 49ers", "Long Beach State"])
  df_alt_names.append(["Portland Pilots", "Portland"])
  df_alt_names.append(["Pacific Tigers", "Pacific"])
  df_alt_names.append(["Santa Clara Broncos", "Santa Clara"])
  df_alt_names.append(["Pepperdine Waves", "Pepperdine"])
  df_alt_names.append(["Weber State Wildcats", "Weber State"])
  df_alt_names.append(["Portland St Vikings", "Portland State"])
  df_alt_names.append(["Saint Mary's Gaels", "Saint Mary's"])
  df_alt_names.append(["San Diego Toreros", "San Diego"])
  df_alt_names.append(["Arizona Wildcats", "Arizona"])
  df_alt_names.append(["Utah Utes", "Utah"])
  df_alt_names.append(["USC Trojans", "USC"])
  df_alt_names.append(["Oregon St Beavers", "Oregon State"])
  df_alt_names.append(["Cal Poly Mustangs", "Cal Poly"])
  df_alt_names.append(["Hawai'i Rainbow Warriors", "Hawai'i"])
  df_alt_names.append(["Akron Zips", "Akron"])
  df_alt_names.append(["Ohio Bobcats", "Ohio"])
  df_alt_names.append(["Canisius Golden Griffins", "Canisius"])
  df_alt_names.append(["Iona Gaels", "Iona"])
  df_alt_names.append(["Manhattan Jaspers", "Manhattan"])
  df_alt_names.append(["Marist Red Foxes", "Marist"])
  df_alt_names.append(["Northwestern Wildcats", "Northwestern"])
  df_alt_names.append(["Penn State Nittany Lions", "Penn State"])
  df_alt_names.append(["Saint Louis Billikens", "Saint Louis"])
  df_alt_names.append(["Richmond Spiders", "Richmond"])
  df_alt_names.append(["Iowa Hawkeyes", "Iowa"])
  df_alt_names.append(["Nebraska Cornhuskers", "Nebraska"])
  df_alt_names.append(["San Jos?? St Spartans", "San Jos???? State"])
  df_alt_names.append(["Saint Peter's Peacocks", "Saint Peter's"])
  df_alt_names.append(["Monmouth Hawks", "Monmouth"])
  df_alt_names.append(["Niagara Purple Eagles", "Niagara"])
  df_alt_names.append(["Rider Broncs", "Rider"])
  df_alt_names.append(["Harvard Crimson", "Harvard"])
  df_alt_names.append(["Princeton Tigers", "Princeton"])
  df_alt_names.append(["Florida Gators", "Florida"])
  df_alt_names.append(["Georgia Bulldogs", "Georgia"])
  df_alt_names.append(["Purdue Boilermakers", "Purdue"])
  df_alt_names.append(["Michigan St Spartans", "Michigan State"])
  df_alt_names.append(["Oklahoma St Cowboys", "Oklahoma State"])
  df_alt_names.append(["Oklahoma Sooners", "Oklahoma"])
  df_alt_names.append(["Rhode Island Rams", "Rhode Island"])
  df_alt_names.append(["Butler Bulldogs", "Butler"])
  df_alt_names.append(["Marquette Golden Eagles", "Marquette"])
  df_alt_names.append(["Arkansas Razorbacks", "Arkansas"])
  df_alt_names.append(["Yale Bulldogs", "Yale"])
  df_alt_names.append(["Cornell Big Red", "Cornell"])
  df_alt_names.append(["Pennsylvania Quakers", "Pennsylvania"])
  df_alt_names.append(["Dartmouth Big Green", "Dartmouth"])
  df_alt_names.append(["Dayton Flyers", "Dayton"])
  df_alt_names.append(["Kansas St Wildcats", "Kansas State"])
  df_alt_names.append(["North Carolina Tar Heels", "North Carolina"])
  df_alt_names.append(["North Dakota St Bison", "North Dakota State"])
  df_alt_names.append(["North Dakota Fighting Hawks", "North Dakota"])
  df_alt_names.append(["New Mexico St Aggies", "New Mexico State"])
  df_alt_names.append(["Miami Hurricanes", "Miami"])
  df_alt_names.append(["Eastern Michigan Eagles", "Eastern Michigan"])
  df_alt_names.append(["Ball State Cardinals", "Ball State"])
  df_alt_names.append(["Texas A&M Aggies", "Texas A&M"])
  df_alt_names.append(["Seton Hall Pirates", "Seton Hall"])
  df_alt_names.append(["Air Force Falcons", "Air Force"])
  df_alt_names.append(["Tennessee Volunteers", "Tennessee"])
  df_alt_names.append(["Florida St Seminoles", "Florida State"])
  df_alt_names.append(["Massachusetts Minutemen", "UMass"])
  df_alt_names.append(["Western Michigan Broncos", "Western Michigan"])
  df_alt_names.append(["Bowling Green Falcons", "Bowling Green"])
  df_alt_names.append(["Columbia Lions", "Columbia"])
  df_alt_names.append(["Brown Bears", "Brown"])
  df_alt_names.append(["Rutgers Scarlet Knights", "Rutgers"])
  df_alt_names.append(["Saint Joseph's Hawks", "Saint Joseph's"])
  df_alt_names.append(["Texas Tech Red Raiders", "Texas Tech"])
  df_alt_names.append(["Kent State Golden Flashes", "Kent State"])
  df_alt_names.append(["Louisville Cardinals", "Louisville"])
  df_alt_names.append(["Western Kentucky Hilltoppers", "Western Kentucky"])
  df_alt_names.append(["Kansas Jayhawks", "Kansas"])
  df_alt_names.append(["Baylor Bears", "Baylor"])
  df_alt_names.append(["Stanford Cardinal", "Stanford"])
  df_alt_names.append(["California Golden Bears", "California"])
  df_alt_names.append(["Missouri Tigers", "Missouri"])
  df_alt_names.append(["CSU Bakersfield Roadrunners", "CSU Bakersfield"])
  df_alt_names.append(["UTEP Miners", "UTEP"])
  df_alt_names.append(["Toledo Rockets", "Toledo"])
  df_alt_names.append(["St. Bonaventure Bonnies", "St. Bonaventure"])
  df_alt_names.append(["Denver Pioneers", "Denver"])
  df_alt_names.append(["New Hampshire Wildcats", "New Hampshire"])
  df_alt_names.append(["Lipscomb Bisons", "Lipscomb"])
  df_alt_names.append(["Fairleigh Dickinson Knights", "Fairleigh Dickinson"])
  df_alt_names.append(["NJIT Highlanders", "NJIT"])
  df_alt_names.append(["Florida A&M Rattlers", "Florida A&M"])
  df_alt_names.append(["Grambling St Tigers", "Grambling"])
  df_alt_names.append(["Wagner Seahawks", "Wagner"])
  df_alt_names.append(["Coppin St Eagles", "Coppin State"])
  df_alt_names.append(["Maryland-Eastern Shore Hawks", "Maryland-Eastern Shore"])
  df_alt_names.append(["North Carolina Central Eagles", "North Carolina Central"])
  df_alt_names.append(["Howard Bison", "Howard"])
  df_alt_names.append(["Morgan St Bears", "Morgan State"])
  df_alt_names.append(["Delaware St Hornets", "Delaware State"])
  df_alt_names.append(["Alabama St Hornets", "Alabama State"])
  df_alt_names.append(["Alabama A&M Bulldogs", "Alabama A&M"])
  df_alt_names.append(["South Carolina St Bulldogs", "South Carolina State"])
  df_alt_names.append(["Norfolk St Spartans", "Norfolk State"])
  df_alt_names.append(["Alcorn St Braves", "Alcorn State"])
  df_alt_names.append(["Prairie View Panthers", "Prairie View A&M"])
  df_alt_names.append(["Miss Valley St Delta Devils", "Mississippi Valley State"])
  df_alt_names.append(["Arkansas-Pine Bluff Golden Lions", "Arkansas-Pine Bluff"])
  df_alt_names.append(["Bethune-Cookman Wildcats", "Bethune-Cookman"])
  df_alt_names.append(["Southern Jaguars", "Southern"])
  df_alt_names.append(["Jackson St Tigers", "Jackson State"])
  df_alt_names.append(["Texas Southern Tigers", "Texas Southern"])
  df_alt_names.append(["LIU Sharks", "Long Island University"])
  df_alt_names.append(["UConn Huskies", "UConn"])
  df_alt_names.append(["Michigan Wolverines", "Michigan"])
  df_alt_names.append(["Fairfield Stags", "Fairfield"])
  df_alt_names.append(["George Washington Colonials", "George Washington"])
  df_alt_names.append(["Wichita St Shockers", "Wichita State"])
  df_alt_names.append(["Montana St Bobcats", "Montana State"])
  df_alt_names.append(["Fresno St Bulldogs", "Fresno State"])
  df_alt_names.append(["Villanova Wildcats", "Villanova"])
  df_alt_names.append(["Pittsburgh Panthers", "Pittsburgh"])
  df_alt_names.append(["UT Rio Grande Valley Vaqueros", "UT Rio Grande Valley"])

  df_alt_names = pd.DataFrame(df_alt_names, columns = ['odd_name', 'correct_name'])

  odds_info = []
  today_date = today.strftime("%m-%d-%Y")

  for i in range(len(odds_json)):
    # for i in range(1):
    game_time_info = datetime.datetime.fromtimestamp(odds_json[i]['commence_time'])
    game_time = f"{game_time_info:%H:%M:%S}"
    game_date = f"{game_time_info:%m-%d-%Y}"
    home_team = odds_json[i]['home_team']
    away_team = odds_json[i]['away_team']
    game_info = next((item for item in odds_json[i]['bookmakers'] if item["key"] == "fanduel"), None )
    if(game_info == None or len(game_info['markets']) < 2):
        #If fanduel does not exist use the first to appear in list
        game_info = next((item for item in odds_json[i]['bookmakers']), None )
        if(game_info == None or len(game_info['markets']) < 2):
            print(home_team, away_team)
            continue

    home_odds_ml = next((item['price'] for item in game_info['markets'][0]['outcomes'] if item["name"] == home_team), None)
    away_odds_ml = next((item['price'] for item in game_info['markets'][0]['outcomes'] if item["name"] == away_team), None)
    home_odds_spread = next((item['price'] for item in game_info['markets'][1]['outcomes'] if item["name"] == home_team), None)
    away_odds_spread = next((item['price'] for item in game_info['markets'][1]['outcomes'] if item["name"] == away_team), None)
    home_point_spread = next((item['point'] for item in game_info['markets'][1]['outcomes'] if item["name"] == home_team), None)
    away_point_spread = next((item['point'] for item in game_info['markets'][1]['outcomes'] if item["name"] == away_team), None)
    odds_info.append([game_date,game_time, away_team,away_odds_ml, home_team, home_odds_ml,home_point_spread,home_odds_spread,away_point_spread,away_odds_spread])

  odds_info = pd.DataFrame(odds_info, columns = ['date','game_time', 'away_team','away_odds_ml', 'home_team', 'home_odds_ml','home_point_spread', 'home_odds_spread','away_point_spread', 'away_odds_spread'])
  odds_info['N'] = False
  
  odds_info = odds_info.merge(df_alt_names, how="left", left_on='away_team', right_on="odd_name")
  odds_info['away_team'] = odds_info.apply(lambda x: x.away_team if pd.isna(x.correct_name) else x.correct_name , axis=1)
  odds_info.drop(['odd_name', 'correct_name'], inplace=True, axis=1)

  odds_info = odds_info.merge(df_alt_names, how="left", left_on='home_team', right_on="odd_name")
  odds_info['home_team'] = odds_info.apply(lambda x: x.home_team if pd.isna(x.correct_name) else x.correct_name , axis=1)
  odds_info.drop(['odd_name', 'correct_name'], inplace=True, axis=1)
  return odds_info.to_dict()
  
