use std::{
    io::{BufRead, BufReader, Error},
    process::{Command, Stdio},
};

fn main() {
    let initial_output = Command::new("nmcli")
        .args(["-g", "device, state, connection", "device", "status"])
        .output()
        .expect("Error running initial nmcli")
        .stdout;

    let initial_str = String::from_utf8(initial_output).expect("Error casting buff to str");

    println!("Initial output");
    initial_str.split(' ').for_each(|line| println!("{line}"));

    fn continuous_output() -> Result<(), Error> {
        let continuous_stdout = Command::new("nmcli")
            .args(["device", "monitor"])
            .stdout(Stdio::piped())
            .spawn()?
            .stdout
            .ok_or_else(|| Error::new(std::io::ErrorKind::Other, "Could not capture stdout."))?;

        let reader = BufReader::new(continuous_stdout);

        reader
            .lines()
            .filter_map(|line| line.ok())
            .for_each(|s| println!("{}", s));

        Ok(())
    }

    match continuous_output() {
        Ok(o) =>  o,
        Err(e) => println!("Error! {}", e)
    }
}
