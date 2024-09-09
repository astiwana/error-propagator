## Error Propagation Calculator

My team and I developed this project during the MecSimCalc 2023 Hackathon, where we earned 3rd place in the hackathon.

## Introduction

This tool automatically derives the Gaussian error equation for any inputted equation and calculates the numerical error if provided with the values of variables and their corresponding errors. It's particularly useful for physics courses that involve error analysis.

We used SymPy to parse the input equation, convert it into a symbolic object, and derive partial derivatives for each variable. These derivatives are converted into LaTeX and displayed on the website. The tool then walks through the Gaussian error propagation process, showing step-by-step calculations. The calculator computes and outputs the final numerical error if the user provides variable values and their errors.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
