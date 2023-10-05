const vscode = require('vscode');
const path = require('path');

let lineCount = {};

async function countLinesInDirectory(directory) {
    const entries = await vscode.workspace.fs.readDirectory(directory);

    for (const [name, type] of entries) {
        const fullPath = path.join(directory.fsPath, name);

        if (type === vscode.FileType.Directory) {
            await countLinesInDirectory(vscode.Uri.file(fullPath));
        } else if (type === vscode.FileType.File) {
            const fileExtension = path.extname(name);
            const lang = getFileLanguage(fileExtension);

            if (lang) {
                await countLinesInFile(vscode.Uri.file(fullPath), lang);
            }
        }
    }
}

function getFileLanguage(ext) {
    let langMap = {
        '.c': 'C',
        '.cpp': 'C++',
        '.java': 'Java',
        '.js': 'JavaScript',
        '.py': 'Python',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.go': 'Go',
        '.rs': 'Rust',
        '.kt': 'Kotlin',
        '.ts': 'TypeScript'
    };

    return langMap[ext] || null;
}

async function countLinesInFile(file, lang) {
    const fileContent = (await vscode.workspace.fs.readFile(file)).toString();

    if (!lineCount[lang]) {
        lineCount[lang] = 0;
    }

    lineCount[lang] += fileContent.split('\n').length;
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.countLines', async function () {
        lineCount = {}; // Reset line count

        if (vscode.workspace.workspaceFolders) {
            const rootFolderUri = vscode.workspace.workspaceFolders[0].uri;

            await countLinesInDirectory(rootFolderUri);

            vscode.window.showInformationMessage(`Total lines: ${JSON.stringify(lineCount)}`);
        } else {
            vscode.window.showErrorMessage('No workspace directory is currently open.');
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
};