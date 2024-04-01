pub struct OutputMsg {
    pub icon: char,
    pub text: String,
}

impl OutputMsg {
    pub fn format(self) -> String {
        format!(
            "{{ \"icon\": \"{}\", \"text\": \"{}\"}}",
            self.icon, self.text
        )
    }
}
