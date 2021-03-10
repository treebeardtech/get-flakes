// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode'
import * as child_process from 'child_process'
import {promisify} from 'util'

const exec = promisify(child_process.exec)

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext): void {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "deeptest" is now active!')

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  let disposable = vscode.commands.registerCommand(
    'deeptest.helloWorld',
    async () => {
      // The code you place here will be executed every time your command is executed

      // Display a message box to the user
      vscode.window.showInformationMessage('Hello World from deeptest 42!')
      const openEditor = vscode.window.visibleTextEditors[0]
      const cwd = `${vscode.workspace.workspaceFolders![0].uri.path}/.deeptest`
      const source = openEditor.document.fileName
      const res = await exec(`cd ${cwd} && deeptest ${source}`)
      console.log(res)
      const data = JSON.parse(res.stdout)
      decorate(openEditor, data)
    }
  )

  context.subscriptions.push(disposable)
}

interface Line {
  passed: string[]
  failed: string[]
}

function getContent(line: Line): [string, string] {
  let s = '-'
  let passed = ''
  let failed = ''
  if (line.passed.length > 0) {
    s += `${line.passed.length} passed, `
    passed = `Passed:\n\n${line.passed.join('\n\n')}`
  }

  if (line.failed.length > 0) {
    s += `${line.failed.length} failed`
    failed = `Failed:\n\n${line.failed.join('\n\n')}`
  }

  if (s.length > 0) {
    s += '  in 0.83s'
  }
  s = s.padEnd(45, '-')
  console.log(s.length)
  return [s, [failed, passed].join('\n\n')]
}

function decorate(editor: vscode.TextEditor, data: any): void {
  for (const line of Object.keys(data.lines).map(Number)) {
    let range = new vscode.Range(
      new vscode.Position(line - 1, 0),
      new vscode.Position(line, 0)
    )

    const lineObj = data.lines[`${line}`] as Line
    const [contentText, hoverMessage] = getContent(lineObj)
    const decorationType = vscode.window.createTextEditorDecorationType({
      before: {
        backgroundColor: 'rgba(0,0,0,0.1)',
        color: lineObj.failed.length > 0 ? 'red' : 'rgba(0,0,0,0.75)',
        height: '100%',
        margin: '0 26px -1px 0',
        contentText
      }
    })
    const decoration: vscode.DecorationOptions = {
      hoverMessage,
      range
    }
    editor.setDecorations(decorationType, [decoration])
  }
}

// this method is called when your extension is deactivated
export function deactivate(): void {}
