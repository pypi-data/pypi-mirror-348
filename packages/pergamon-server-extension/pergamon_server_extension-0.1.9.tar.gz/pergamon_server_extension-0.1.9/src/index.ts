import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { INotebookTracker } from '@jupyterlab/notebook';
import { CodeCell } from '@jupyterlab/cells';
import { NotebookActions } from '@jupyterlab/notebook';

const setupCode = `
%load_ext jupyter_ai
%ai register anthropic-chat anthropic-chat:claude-2.0
%ai register native-cohere cohere:command
%ai register bedrock-cohere bedrock:cohere.command-text-v14
%ai register anthropic anthropic:claude-v1
%ai register bedrock bedrock:amazon.titan-text-lite-v1
%ai register gemini gemini:gemini-1.0-pro-001
%ai register gpto openai-chat:gpt-4o
%ai delete ernie-bot
%ai delete ernie-bot-4
%ai delete titan
%load_ext pergamon_server_extension
`;

/**
 * Initialization data for the pergamon_server_extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pergamon_server_extension:plugin',
  description: 'Calliope server extension',
  requires: [INotebookTracker],
  autoStart: true,
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {
    tracker.widgetAdded.connect((sender, notebookPanel) => {
      notebookPanel.sessionContext.ready.then(() => {
        const session = notebookPanel.sessionContext.session;

        if (session?.kernel) {
          session.kernel.registerCommTarget('toggle_fixing', comm => {
            comm.onMsg = msg => {
              const targetCell = notebookPanel.content.activeCell;
              if (targetCell) {
                const codeCell = targetCell as CodeCell;
                if (codeCell.model.sharedModel) {
                  codeCell.node.classList.toggle('calliope-thinking');
                }
              }
            };
          });

          session.kernel.registerCommTarget('toggle_thinking', comm => {
            comm.onMsg = msg => {
              const cells = notebookPanel.content.widgets || [];

              cells.forEach(cell => {
                if (cell) {
                  const codeCell = cell;
                  if (
                    !codeCell ||
                    !codeCell.model ||
                    !codeCell.model.sharedModel ||
                    !codeCell.node
                  ) {
                    return;
                  }

                  const cellContent = codeCell.model.sharedModel.source || '';
                  const hasMagic = cellContent.trim().startsWith('%%calliope');
                  const hasThinkingClass =
                    codeCell.node.classList.contains('calliope-thinking');

                  const isExecuting =
                    codeCell.node.classList.contains('executing');

                  if (hasMagic) {
                    if (isExecuting && !hasThinkingClass) {
                      codeCell.node.classList.add('calliope-thinking');
                    } else if (!isExecuting && hasThinkingClass) {
                      codeCell.node.classList.remove('calliope-thinking');
                    }
                  }
                }
              });
            };
          });

          session?.kernel?.registerCommTarget('replace_cell', comm => {
            comm.onMsg = msg => {
              const newCode = msg.content.data.replace_with as string;
              const activeCell = notebookPanel.content.activeCell;

              if (activeCell && activeCell.model.type === 'code') {
                const codeCell = activeCell as CodeCell;
                if (codeCell.editor) {
                  codeCell.model.sharedModel.setSource(newCode);
                  NotebookActions.run(
                    notebookPanel.content,
                    notebookPanel.sessionContext
                  );
                }
              }
            };
          });
          // loads the extension
          session.kernel
            .requestExecute({
              code: setupCode
            })
            .done.then(() => {});
        }

        const notebook = notebookPanel.content;

        notebookPanel.context.sessionContext.statusChanged.connect(
          (_, status) => {
            if (status === 'busy') {
              const active = notebook.activeCell;
              if (active) {
                active.node.classList.add('executing');
              }
            }

            if (status === 'idle') {
              notebook.widgets.forEach(cell => {
                cell.node.classList.remove('executing');
                cell.node.classList.remove('calliope-thinking');
              });
            }
          }
        );
      });
    });

    const observer = new MutationObserver((mutationsList, observer) => {
      const splashElement = document.querySelector('.jp-Splash');
      if (splashElement) {
        splashElement.remove();
        observer.disconnect();
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }
};

export default plugin;
