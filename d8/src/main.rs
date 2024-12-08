use std::fs;
use std::collections::HashMap;

fn main() {
    let test = true;
    let path = if test {"./test.txt"} else {"./real.txt"};
    let mut content = fs::read_to_string(path).unwrap();
    let lines: Vec<_> = content.split("\n").filter(|l| !l.is_empty()).collect();
    let lines_count = lines.len(); 
    let line_len = lines[0].len();
    let mut positions = HashMap::new();
    for i in 0..lines_count {
        for j in 0..line_len {
            let c = lines[i][j];
            let exists = positions.contains_key(c);
            if exists {
                positions.insert(c, vec![(i,j)]);
            } else {
                let mut v = positions.get(k);
                v.push()
            }
        }
    }
    println!("Hello, world!");
}
