Contributing to the Community Air Quality Project

Thank you for your interest in contributing!
This project is an open-source effort to create accessible, low-cost, community-powered air quality monitoring and purification tools.
All skill levels are welcome — whether you're helping with documentation, firmware, hardware, design, data, or community support.


---

🧭 How to Contribute

1. Fork + Clone the Repository

git fork https://github.com/YOUR_ORG/CommunityAirProject.git
git clone https://github.com/YOUR_USERNAME/CommunityAirProject.git
cd CommunityAirProject

2. Create a New Branch

Use a descriptive branch name:

git checkout -b fix-sensor-reading

3. Submit a Pull Request (PR)

Keep PRs focused and specific

Link any related issues

Include screenshots, logs, or schematics if relevant

Make sure your branch is up to date with main



---

🧪 Code Standards

Firmware (C/C++ for ESP32)

Follow Arduino / ESP-IDF formatting rules

Keep all hardware-specific code inside src/hardware/

All new features must include:

inline documentation

error handling

a minimal test scenario



Python Tools / Scripts

Use clear function names

Prefer type hints

Provide an example command in the script header


Markdown Documentation

Place docs in /docs

Use relative links

Keep paragraphs short for readability



---

🛠 Hardware Contribution Guidelines

Before submitting:

Include a schematic PDF

Include parts list (BOM)

Verify wiring against:

ESP32 pinout

PM2.5 sensor datasheet

VOC sensor datasheet


Clearly label:

power requirements

optional components

jumper settings



If adding a new enclosure or 3D printable part:

Provide .STL or .STEP

Include a rendered preview

Document required screws or inserts



---

🎨 Design / Branding Contributions

We welcome:

Logo variations

Infographics

Community training materials

Printable workshop guides


All design assets go in:

/assets/branding
/assets/graphics

Please export vector files as SVG + PNG.


---

📊 Data Contributions

If contributing data analysis or calibration curves:

Include notebooks in /analysis/

Remove personal data

Document:

sensor model

location type (indoor/outdoor/general region)

environmental notes




---

🧰 Reporting Issues

Please include:

a clear description

expected vs. actual behavior

steps to reproduce

hardware model

firmware version

logs if available


Use the Issue Templates in .github/ISSUE_TEMPLATE/.


---

👐 Community Code of Conduct

All contributors must follow the Code of Conduct (included separately).
We value:

respect

collaboration

accessibility

scientific integrity



---

🙌 Thank You

Your contributions help build cleaner, healthier air systems for communities everywhere.
If you have any questions, feel free to open a Discussion on GitHub.
