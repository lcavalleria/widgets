use std::io::{BufRead, BufReader, Error};
use std::process::{Command, Stdio};

pub struct Nmcli {}

impl Nmcli {
    pub fn initial_string() -> String {
        let initial_output = Command::new("nmcli")
            .args(["-g", "device, state, connection", "device", "status"])
            .output()
            .expect("Error running initial nmcli")
            .stdout;

        String::from_utf8(initial_output).expect("Error casting buff to str")
    }

    pub fn continuous_output() -> Result<Iterator<jaja xd>, Error> { // TODO: no em deixa retornar un iter.
        // Investigar
        let continuous_stdout = Command::new("nmcli")
            .args(["device", "monitor"])
            .stdout(Stdio::piped())
            .spawn()?
            .stdout
            .ok_or_else(|| Error::new(std::io::ErrorKind::Other, "Could not capture stdout."))?;

        let reader = BufReader::new(continuous_stdout);

        // Get continuous_output iterator
        let continuous_output_iter = reader.lines().filter_map(|line| line.ok());

        Ok(continuous_output_iter)
    }
}
