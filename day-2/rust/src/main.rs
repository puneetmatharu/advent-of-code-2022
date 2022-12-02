use std::collections::HashMap;
use std::fs;

#[derive(PartialEq, Copy, Clone)]
enum Outcome {
    Lose = 0,
    Draw = 3,
    Win = 6,
}

#[derive(PartialEq, Copy, Clone)]
enum Move {
    Rock = 1,
    Paper = 2,
    Scissors = 3,
}

//  Cyclic array; A beats B, B beats C, C beats A
static CYCLE: [Move; 3] = [Move::Rock, Move::Scissors, Move::Paper];

fn move_that_beats(mv: &Move) -> Move {
    let mut index: i8 = CYCLE.iter().position(|r| *r == *mv).unwrap() as i8;
    index = (index - 1) % 3;
    index = if index < 0 { index + 3 } else { index };
    CYCLE[index as usize]
}

fn move_that_loses(mv: &Move) -> Move {
    let mut index: i8 = CYCLE.iter().position(|r| *r == *mv).unwrap() as i8;
    index = (index + 1) % 3;
    index = if index < 0 { index + 3 } else { index };
    CYCLE[index as usize]
}

fn does_beat(your_move: &Move, their_move: &Move) -> bool {
    their_move == &move_that_loses(your_move)
}

fn get_outcome(their_move: &Move, your_move: &Move) -> Outcome {
    if your_move == their_move {
        Outcome::Draw
    } else if does_beat(your_move, their_move) {
        Outcome::Win
    } else {
        Outcome::Lose
    }
}

fn get_desired_move(their_move: &Move, your_outcome: &Outcome) -> Move {
    if your_outcome == &Outcome::Draw {
        *their_move
    } else if your_outcome == &Outcome::Win {
        move_that_beats(their_move)
    } else {
        move_that_loses(their_move)
    }
}

fn solve_pt1(data: &[[String; 2]]) -> u64 {
    let letter_to_their_move =
        HashMap::from([("A", Move::Rock), ("B", Move::Paper), ("C", Move::Scissors)]);
    let letter_to_your_move =
        HashMap::from([("X", Move::Rock), ("Y", Move::Paper), ("Z", Move::Scissors)]);

    let mut total_score: u64 = 0;
    for s in data.iter() {
        let their_move: &Move = letter_to_their_move.get(&s[0] as &str).unwrap();
        let your_move: &Move = letter_to_your_move.get(&s[1] as &str).unwrap();
        let your_outcome: Outcome = get_outcome(their_move, your_move);
        total_score += your_outcome as u64 + *your_move as u64;
    }
    total_score
}

fn solve_pt2(data: &[[String; 2]]) -> u64 {
    let letter_to_their_move =
        HashMap::from([("A", Move::Rock), ("B", Move::Paper), ("C", Move::Scissors)]);
    let letter_to_your_outcome = HashMap::from([
        ("X", Outcome::Lose),
        ("Y", Outcome::Draw),
        ("Z", Outcome::Win),
    ]);

    let mut total_score: u64 = 0;
    for s in data.iter() {
        let their_move: &Move = letter_to_their_move.get(&s[0] as &str).unwrap();
        let your_outcome: &Outcome = letter_to_your_outcome.get(&s[1] as &str).unwrap();
        let your_move: Move = get_desired_move(their_move, your_outcome);
        total_score += *your_outcome as u64 + your_move as u64;
    }
    total_score
}

fn load(fname: &str) -> Vec<[String; 2]> {
    fs::read_to_string(fname)
        .unwrap()
        .lines()
        .map(|x| {
            x.split(' ')
                .map(|y| y.to_string())
                .collect::<Vec<String>>()
                .try_into()
                .unwrap()
        })
        .collect::<Vec<_>>()
}

fn main() {
    let example_data = load("./../data/example.dat");
    let test_data = load("./../data/test.dat");

    println!("[EXAMPLE] Answer pt.1: {}", solve_pt1(&example_data));
    println!("[EXAMPLE] Answer pt.2: {}", solve_pt2(&example_data));
    println!("[TEST] Answer pt.1: {}", solve_pt1(&test_data));
    println!("[TEST] Answer pt.2: {}", solve_pt2(&test_data));
}
