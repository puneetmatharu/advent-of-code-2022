use std::fs;

fn solve_pt1(text: &str) -> u64 {
    0
}

fn solve_pt2(text: &str) -> u64 {
    0
}

fn load(fname: String) -> String {
    fs::read_to_string(fname).expect("Unable to load data!")
}

fn main() {
    let example_data = load(String::from("./../data/example.dat"));
    let test_data = load(String::from("./../data/test.dat"));

    println!("[EXAMPLE] Answer pt.1: {}", solve_pt1(&example_data));
    // println!("[EXAMPLE] Answer pt.2: {}", solve_pt2(&example_data));
    // println!("[TEST] Answer pt.1: {}", solve_pt1(&test_data));
    // println!("[TEST] Answer pt.2: {}", solve_pt2(&test_data));
}
