use lobby::{q1, q2};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <filename>", args[0]);
        std::process::exit(2);
    }
    let filename = &args[1];

    match q1(filename) {
        Ok(r) => println!("q1: {}", r),
        Err(e) => eprintln!("q1 error: {}", e),
    }

    match q2(filename) {
        Ok(r) => println!("q2: {}", r),
        Err(e) => eprintln!("q2 error: {}", e),
    }
}

