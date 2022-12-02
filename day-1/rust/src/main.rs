use std::fs;

fn solve_pt1(text: &str) -> u32 {
    let cals_per_elf: Vec<u32> = text
        .split("\n\n")
        .map(|x| x.split('\n').map(|y| y.parse::<u32>().unwrap()).sum())
        .collect();
    return *cals_per_elf.iter().max().unwrap();
}

fn solve_pt2(text: &str) -> u64 {
    let mut cals_per_elf: Vec<u64> = text
        .split("\n\n")
        .map(|x| x.split('\n').map(|y| y.parse::<u64>().unwrap()).sum())
        .collect();
    cals_per_elf.sort();
    return cals_per_elf.iter().rev().take(3).sum::<u64>();
}

fn load(fname: String) -> String {
    fs::read_to_string(fname).expect("Unable to load data!")
}

fn main() {
    let example_data = load(String::from("./../data/example.dat"));
    let test_data = load(String::from("./../data/test.dat"));

    let enable_example2: bool = true;
    let enable_test1: bool = true;
    let enable_test2: bool = true;

    println!("[EXAMPLE] Answer pt.1: {}", solve_pt1(&example_data));

    if enable_example2 {
        println!("[EXAMPLE] Answer pt.2: {}", solve_pt2(&example_data));
    }

    if enable_test1 {
        println!("[TEST] Answer pt.1: {}", solve_pt1(&test_data));
    }

    if enable_test2 {
        println!("[TEST] Answer pt.2: {}", solve_pt2(&test_data));
    }
}
