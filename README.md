
# Pathways Task Reminder

A streamlit app to convert student updates into images to serve as reminders
of remaining tasks.

## Features

1. Extracts tables from uploaded PDFs.
2. Displays the first table in the PDF as an image.
3. Allows downloading the table image.

## Installation

If running locally, install package `wkhtmltopdf`

```
# ubuntu/debian
sudo apt-get wkhtmltopdf
# arch
yay -S wkhtmltopdf-static
```

1. Clone the repository:
   ```bash
   git clone https://github.com/jtprince/pathways-task-reminder.git
   cd pathways-task-reminder

