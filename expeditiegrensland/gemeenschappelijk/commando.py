import logging
import subprocess


def draai_pijp(commandos, logger):
    logger.debug("Volledig commando:\n" + " | \n".join(map(str, commandos)))

    processen = None

    for commando in commandos:
        if not processen:
            processen = [subprocess.Popen(commando, stdout=subprocess.PIPE)]
        else:
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


def draai(commando, logger):
    return draai_pijp([commando], logger)
