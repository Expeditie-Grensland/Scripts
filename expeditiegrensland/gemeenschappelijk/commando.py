import logging
import subprocess
import shutil


def draai_pijp(commandos: list[list[str]]):
    logger = logging.getLogger("__main__")
    logger.debug("Volledig commando:\n" + " | \n".join(map(str, commandos)))

    processen = [subprocess.Popen(commandos[0], stdout=subprocess.PIPE)]

    for commando in commandos[1:]:
        processen.append(
            subprocess.Popen(
                commando, stdin=processen[-1].stdout, stdout=subprocess.PIPE
            )
        )

    stdout = processen[-1].communicate()[0]
    stdout = stdout.decode("utf-8", "replace")
    logger.debug("Programma-uitvoer:\n" + stdout.strip())

    if processen[-1].returncode != 0:
        raise Exception("Programma sloot af met een fout")
    return stdout


def draai(commando: list[str]):
    return draai_pijp([commando])


def vereis_programma(programma: str, programma_naam: str | None = None):
    if shutil.which(programma) is None:
        naam = f"'${programma}'"
        if programma_naam:
            naam += f" (van ${programma_naam})"

        raise Exception(f"Dit programma benodigd ${naam}")
