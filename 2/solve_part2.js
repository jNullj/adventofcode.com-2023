let fs = require("node:fs")
let data = fs.readFileSync(__dirname+"/input.txt", {encoding: 'utf8'})
let data_arr = data.split("\n")
let games = { }
for (let i = 0; i < data_arr.length; i++ ) {
    const [,
        game_num,
        game_results,
    ] = data_arr[i].match(
        /Game ([0-9]+):(.*)/
    ) ?? [null, null]
    if (!game_num) { continue }
    const game_resuls_arr = game_results.split(';')
    for (j = 0; j < game_resuls_arr.length; j++) {
        games[parseInt(game_num)] = games[parseInt(game_num)] || { }
        games[parseInt(game_num)][j] = {
            red: parseInt((game_resuls_arr[j].match(/([0-9]+) red/) || [null, 0])[1]),
            green: parseInt((game_resuls_arr[j].match(/([0-9]+) green/) || [null, 0])[1]),
            blue: parseInt((game_resuls_arr[j].match(/([0-9]+) blue/) || [null, 0])[1]),
        }
    }
}

sum = 0
Object.entries(games).forEach(([game_num, game]) => {
    game_num = parseInt(game_num)
    let max_red = 0
    let max_green = 0
    let max_blue = 0
    Object.values(game).forEach(game_throw => {
        max_red = game_throw.red > max_red       ? game_throw.red : max_red
        max_green = game_throw.green > max_green ? game_throw.green : max_green
        max_blue = game_throw.blue > max_blue    ? game_throw.blue : max_blue
    })
    const power_of_cubes = max_red * max_green * max_blue
    sum += power_of_cubes
})
console.log(sum)
