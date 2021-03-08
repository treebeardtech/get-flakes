// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "deeptest" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('deeptest.helloWorld', () => {
        // The code you place here will be executed every time your command is executed

        // Display a message box to the user
        vscode.window.showInformationMessage('Hello World from deeptest 42!');
        const openEditor = vscode.window.visibleTextEditors[0]
        decorate(openEditor)
    });

    context.subscriptions.push(disposable);
}

const decorationType = vscode.window.createTextEditorDecorationType({
    before: {
        backgroundColor: 'rgba(0,0,0,0.1)',
        color: 'rgba(0,0,0,0.75)',
        height: '100%',
        margin: '0 26px -1px 0',
        contentText: "🟢 ₅ ❌ ₂"
    },
  })

function decorate(editor: vscode.TextEditor) {
    let sourceCode = editor.document.getText()
    let regex = /(console\.log)/

    let decorationsArray: vscode.DecorationOptions[] = []

    const sourceCodeArr = sourceCode.split('\n')

    for (let line = 0; line < sourceCodeArr.length; line++) {
        let match = sourceCodeArr[line].match(regex)

        if (match !== null && match.index !== undefined) {
            let range = new vscode.Range(
                new vscode.Position(line, match.index),
                new vscode.Position(line, match.index + match[1].length)
            )

            let decoration = { range }

            decorationsArray.push(decoration)
        }
    }

    editor.setDecorations(decorationType, decorationsArray)
}

// this method is called when your extension is deactivated
export function deactivate() {}
