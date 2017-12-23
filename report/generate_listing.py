import os


def get_folder_names(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()
    return folders


paths = [".1 root/."]
full_paths = []
counter = 1
last_dir = None
for root, dirs, files in os.walk("..", topdown=False):
    if "report" in root:
        continue

    for file_name in files:
        if file_name.endswith(".py") and "__init__" not in file_name:
            if last_dir != root and len(paths) > 1:
                counter -= 1
                last_dir = root

            new_path = os.path.join(root, file_name)[3:]
            while counter < new_path.count("/") + new_path.count("\\") + 1:
                counter += 1
                paths.append(".{} {}.".format(counter, get_folder_names(new_path)[counter - 2] + "/"))
            while counter > new_path.count("/") + new_path.count("\\") + 1:
                counter -= 1
            paths.append(".{} {}.".format(counter + 1, file_name))
            full_paths.append(os.path.join(root, file_name))

# Deduplicate path list
paths = list(dict.fromkeys(paths))

# Generate directory tree visualization
DIR_STRUCTURE_TEX = r"""
\dirtree{%%
%s
}
""" % "\n".join(paths).replace("_", "\\_")

# Write out code listings
file_listings = []
for path in full_paths:
    code_lines = open(path, "r").readlines()
    # code_lines = [line.replace("\\", "\\\\") for line in code_lines]

    file_listings.append(r"""\subsection{%s}
\begin{lstlisting}
%s
\end{lstlisting}
    """ % (path[3:].replace("\\", " > ").replace("_", "\\_"), "".join(code_lines)))

# Write out the whole thing
TEX = r"""\chapter{Source Code Listing}
\begin{framed}
\centering
Please access the full repository at
\url{https://github.com/gandreadis/danger-zone}
\end{framed}

\section{Directory Structure}
\begin{figure}[H]
%s
\caption{The directory structure of the source code repository. Note: Only Python files appear in this list - for the 
full directory structure, please refer to our GitHub repository.}
\end{figure}

\section{Source Code Files}
%s
""" % (DIR_STRUCTURE_TEX, "\n\n".join(file_listings))

out = open(os.path.join("chapters", "listing.tex"), "w")
out.write(TEX)
