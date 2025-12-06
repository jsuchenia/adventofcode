use std::fs;
use std::io;
use std::path::Path;
use std::str::FromStr;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Direction {
    Forward,
    Backward,
}

impl FromStr for Direction {
    type Err = io::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let ch = s.chars().next().ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidData, "missing direction char")
        })?;

        match ch {
            'R' | '+' | 'r' => Ok(Direction::Forward),
            'L' | '-' | 'l' => Ok(Direction::Backward),
            other => Err(io::Error::new(
                io::ErrorKind::InvalidData,
                format!("unexpected direction char: {}", other),
            )),
        }
    }
}

fn parse_changes<P: AsRef<Path>>(filename: P) -> io::Result<Vec<i64>> {
    let s = fs::read_to_string(filename)?;

    s.lines()
        .map(str::trim)
        .filter(|l| !l.is_empty())
        .map(|line| {
            // split into direction char and numeric part
            let (dir_part, num_part) = line.split_at(1);
            let dir = Direction::from_str(dir_part)?;
            let n: i64 = num_part
                .trim()
                .parse()
                .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;

            Ok(match dir {
                Direction::Forward => n,
                Direction::Backward => -n,
            })
        })
        .collect()
}

/// Count how many times the position lands exactly on 0 (mod 100) after applying each change.
pub fn q1<P: AsRef<Path>>(filename: P) -> io::Result<i64> {
    let changes = parse_changes(filename)?;

    // fold state is (position, count)
    let (_pos, count) = changes.into_iter().fold((50i64, 0i64), |(pos, count), delta| {
        let next = (pos + delta).rem_euclid(100);
        (next, count + if next == 0 { 1 } else { 0 })
    });

    Ok(count)
}

fn count_crossings(start: i64, delta: i64) -> i64 {
    // Follow the Python logic exactly: after moving to `end`,
    // add 1 if end==0, add full 100-cycles, then add booleans that check
    // whether the remainder portion crosses zero based on the final `end` value.
    let end = (start + delta).rem_euclid(100);
    let mut crossings = 0i64;

    if end == 0 {
        crossings += 1;
    }

    crossings += (delta.abs() / 100) as i64;

    let rem = (delta.abs() % 100) as i64;

    if delta > 0 {
        // Python: change > 0 and current < (change % 100) and current != 0
        if rem > 0 && end < rem && end != 0 {
            crossings += 1;
        }
    } else if delta < 0 {
        // Python: change < 0 and current > 100 - (abs(change) % 100)
        if rem > 0 && end > 100 - rem {
            crossings += 1;
        }
    }

    crossings
}

/// More involved counting: includes exact landings, full 100-steps, and remainder-crossings.
pub fn q2<P: AsRef<Path>>(filename: P) -> io::Result<i64> {
    let changes = parse_changes(filename)?;

    let (_pos, count) = changes.into_iter().fold((50i64, 0i64), |(pos, count), delta| {
        let c = count_crossings(pos, delta);
        let next = (pos + delta).rem_euclid(100);
        (next, count + c)
    });

    Ok(count)
}

#[cfg(test)]
mod tests {
    use super::{q1, q2};

    #[test]
    fn test_q1_files() {
        // expected values from the Python tests
        assert_eq!(q1("test.txt").unwrap(), 3);
        assert_eq!(q1("data.txt").unwrap(), 982);
    }

    #[test]
    fn test_q2_files() {
        assert_eq!(q2("test.txt").unwrap(), 6);
        assert_eq!(q2("data.txt").unwrap(), 6106);
    }
}
