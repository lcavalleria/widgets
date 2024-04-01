mod network_info;
mod nmcli_cmds;
mod output_msg;
mod status_icons;

use network_info::NetworkInfo;
use nmcli_cmds::Nmcli;

fn main() {
    // Print initial output
    let mut status = NetworkInfo::create();
    Nmcli::initial_string()
        .split('\n')
        .filter(|line| !line.is_empty())
        .for_each(|line| status.update_from_initial_line(line));
    let output_msg = status.format_output_msg();
    println!("{}", output_msg.format());

    match Nmcli::continuous_output() {
        Ok(c_o) => c_o.for_each(|line| {
            status.update_from_monitor_line(line);
            let output_msg = status.format_output_msg();
            println!("{}", output_msg.format());
        }),
        Err(e) => println!("Error! {}", e),
    }
}
