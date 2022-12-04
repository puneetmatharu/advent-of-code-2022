use itertools::Itertools;
use std::collections::HashSet;

fn char_to_u8(c: char) -> u8 {
    (c as u8) - if c.is_uppercase() { 38 } else { 96 }
}

fn str_to_set(s: &str) -> HashSet<char> {
    s.chars().collect::<HashSet<char>>()
}

fn solve_pt1(text: &str) -> u64 {
    text.lines()
        .map(|s| {
            let (a, b) = s.split_at(s.len() / 2);
            char_to_u8(*str_to_set(a).intersection(&str_to_set(b)).next().unwrap()) as u64
        })
        .sum()
}

fn solve_pt2(text: &str) -> u64 {
    let mut sum: u64 = 0;
    for (a, b, c) in text.lines().tuples() {
        let sets = [str_to_set(a), str_to_set(b), str_to_set(c)];
        let mut iter = sets.into_iter();
        let intersection = iter
            .next()
            .map(|set| iter.fold(set, |set1, set2| (&set1) & (&set2)))
            .unwrap();
        sum += char_to_u8(*intersection.iter().next().unwrap()) as u64;
    }
    sum
}

fn main() {
    let example_data: String = String::from(include_str!("./../../data/example.dat"));
    let test_data: String = String::from(include_str!("./../../data/test.dat"));

    println!("[EXAMPLE] Answer pt.1: {}", solve_pt1(&example_data));
    println!("[TEST] Answer pt.1: {}", solve_pt1(&test_data));
    println!("[EXAMPLE] Answer pt.2: {}", solve_pt2(&example_data));
    println!("[TEST] Answer pt.2: {}", solve_pt2(&test_data));
}
