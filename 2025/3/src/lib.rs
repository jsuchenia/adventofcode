use std::fs;
use std::io;
use std::path::Path;

fn get_data<P: AsRef<Path>>(filename: P) -> io::Result<Vec<String>> {
    let s = fs::read_to_string(filename)?;
    Ok(s.lines().map(|l| l.trim().to_string()).filter(|l| !l.is_empty()).collect())
}

fn find_max_number(bank: &str, size: usize) -> u128 {
    // parse digits safely from bytes (avoid repeated to_digit unwraps)
    let numbers: Vec<u8> = bank
        .as_bytes()
        .iter()
        .filter_map(|b| b.checked_sub(b'0'))
        .map(|d| if d <= 9 { d } else { 255 })
        .filter(|&d| d != 255)
        .collect();

    let mut result: u128 = 0;
    let mut start = 0usize;
    let len = numbers.len();

    // For each digit we need to select (size times), look in a sliding window and
    // pick the first occurrence of the maximal digit. A plain loop is clear and
    // avoids allocations or extra iterator complexity.
    for pick_idx in 0..size {
        let remaining = size - pick_idx - 1;
        let window_end = len - remaining;

        // find first max in numbers[start..window_end]
        let mut best = numbers[start];
        let mut best_rel = 0usize;
        for (i, &v) in numbers[start..window_end].iter().enumerate() {
            if v > best {
                best = v;
                best_rel = i;
                if best == 9 { break; } // early exit - can't get higher than 9
            }
        }

        result = result * 10 + best as u128;
        start += best_rel + 1;
    }

    result
}

pub fn q1<P: AsRef<Path>>(filename: P) -> io::Result<u128> {
    let banks = get_data(filename)?;
    Ok(banks.into_iter().map(|b| find_max_number(&b, 2)).sum())
}

pub fn q2<P: AsRef<Path>>(filename: P) -> io::Result<u128> {
    let banks = get_data(filename)?;
    Ok(banks.into_iter().map(|b| find_max_number(&b, 12)).sum())
}

#[cfg(test)]
mod tests {
    use super::{q1, q2};

    #[test]
    fn test_q1() {
        assert_eq!(q1("test.txt").unwrap(), 357);
        assert_eq!(q1("data.txt").unwrap(), 17346);
    }

    #[test]
    fn test_q2() {
        assert_eq!(q2("test.txt").unwrap(), 3121910778619u128);
        assert_eq!(q2("data.txt").unwrap(), 172981362045136u128);
    }
}
