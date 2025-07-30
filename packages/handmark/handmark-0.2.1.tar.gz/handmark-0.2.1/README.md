# Handmark

Handmark is a Python CLI tool that converts handwritten notes from images into Markdown files. It uses AI to process the images and extract the text.

## Features

* Converts images of handwritten notes to Markdown.
* Simple CLI interface.
* Uses Azure AI for image processing.

## Installation


```bash
pip install handmark
```

## Usage

To use Handmark, run the following command in your terminal:

```bash
handmark --image <image_path>
```

Replace `<image_path>` with the path to the image file you want to convert. The output will be saved as `response.md` in the current directory.


### GitHub Token Configuration (`handmark conf`)

Handmark requires a GitHub token to access the AI model for image processing. You must configure this token before using the tool for the first time.

To set up your token, run:

```bash
handmark conf
```

This command will prompt you to enter your GitHub token securely. The token will be saved in a `.env` file in your project directory as `GITHUB_TOKEN`. This is required for authentication with the AI service. If the token is missing or invalid, Handmark will not work and will display an error message.

You can update or reconfigure your token at any time by running `handmark conf` again.

### Example

Input image (`samples/prova.jpeg`):

![Handwritten notes example](samples/prova.jpeg)

Output (`prova-response.md`):

```markdown
# Primeiro Exercício Escolar - 2025.1

```text
Leia atentamente todas as questões antes de começar a prova. As respostas obtidas somente terão validade se respondidas nas folhas entregues. Os cálculos podem ser escritos a lápis e em qualquer ordem. Evite usar material eletrônico durante a prova, não sendo permitido o uso de calculadora programável para validá-lo. Não é permitido o uso de celular em sala.

---

1. (2 pontos) Determine a equação do plano tangente à função f(x,y) = √(20 - x² - 7y²) em (2,1). Em seguida, calcule um valor aproximado para f(1.9, 1.1).

2. (2 pontos) Determine a derivada direcional de f(x,y) = (xy)^(1/2) em P(2,2), na direção de Q(5,4).

3. (2 pontos) Determine e classifique os extremos de f(x,y) = x⁴ + y⁴ - 4xy + 2.

4. (2 pontos) Usando integrais duplas, calcule o volume acima de onde z = 0 e abaixo da superfície z = x² + y² + 2.

5. (2 pontos) Sabendo que E é o volume do sólido delimitado pelo cilindro parabólico z = x² + y² e pelo plano z = 1, apresente um esboço deste volume e calcule o valor de E.
```

```latex
∫∫ x² e^z dV.
```
```

[Link to prova-response.md](prova-response.md)

## Development

This project uses `uv` for package management.

### Setup

To get started with Handmark, simply install it using pip:

```bash
pip install handmark
```

You do not need to clone the repository or install dependencies manually. After installation, configure your GitHub token as described above, and you are ready to use the CLI.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
