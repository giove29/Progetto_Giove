import subprocess

inputs = ["2", "economisti_1.txt", "avalanche_1.txt", "5"]

process = subprocess.Popen(['python3', 'main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

try:
    for input_value in inputs:
        
        # Invia il valore di input al programma
        process.stdin.write(input_value + '\n')
        process.stdin.flush()  # Garantisce l'invio immediato

    # Leggi il resto dell'output alla fine
    output = process.stdout.read()
    print(output)

    # Attende che il processo termini
    process.wait()

except Exception as e:
    print(f"Errore: {e}")
finally:
    process.terminate()
