function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

all_answers = {}; 
day = 1; 
year = 2024; 
for (let day = 1; day < 26; day++) {
    url = `https://adventofcode.com/${year}/day/${day}`;
    fetch(url).then(response => response.text()).then(function(text) {all_answers[year+''+day] = extract(text)})
    console.log(url);
    sleep(1000);
}
