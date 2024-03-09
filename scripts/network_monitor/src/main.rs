mod nmcli_cmds;
use nmcli_cmds::Nmcli;

fn main() {
    let nmcli: Nmcli = Nmcli {};

    // Print initial output
    nmcli
        .continuous_output
        .split(' ')
        .for_each(|line| println!("{line}"));

    match nmcli.continuous_output {
        Ok(c_o) => c_o.for_each(|s| println!("{}", s)),
        Err(e) => println!("Error! {}", e),
    }
}
