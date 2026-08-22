"""
Motor de conversión de bases numéricas y aritmética de bajo nivel.
Todos los algoritmos están implementados manualmente (sin int(x, base)
ni funciones de conversión nativas del lenguaje).
"""

HEX_DIGITS = "0123456789ABCDEF"


def char_to_value(char):
    """Mapea un carácter ('0'-'9', 'A'-'F') a su valor numérico (0-15)."""
    char = char.upper()
    for i in range(len(HEX_DIGITS)):
        if HEX_DIGITS[i] == char:
            return i
    raise ValueError(f"Carácter inválido: '{char}'")


def value_to_char(value):
    """Mapea un valor numérico (0-15) a su carácter ('0'-'9', 'A'-'F')."""
    return HEX_DIGITS[value]


def to_decimal(number_str, base):
    """
    Cualquier base -> Base 10.
    Teorema fundamental de la numeración:
    suma de (digito * base^posicion)
    """
    number_str = number_str.strip().upper()
    if number_str == "":
        raise ValueError("El número no puede estar vacío")

    result = 0
    power = 0
    for char in reversed(number_str):
        digit = char_to_value(char)
        if digit >= base:
            raise ValueError(f"Dígito '{char}' no válido para base {base}")
        result += digit * (base ** power)
        power += 1
    return result


def from_decimal(number, base):
    """
    Base 10 -> Cualquier base.
    Divisiones sucesivas por la base destino, guardando residuos
    y revirtiendo el arreglo al final.
    """
    if number == 0:
        return "0"

    residuos = []
    n = number
    while n > 0:
        residuo = n % base
        residuos.append(value_to_char(residuo))
        n = n // base

    residuos.reverse()
    return "".join(residuos)


def bits_necesarios(word_size, base):
    """Cantidad de dígitos requeridos para representar word_size bits en 'base'."""
    if base == 2:
        return word_size
    if base == 8:
        return -(-word_size // 3)   # ceil(word_size / 3)
    if base == 16:
        return -(-word_size // 4)   # ceil(word_size / 4)
    return len(from_decimal((2 ** word_size) - 1, base))  # decimal


def validar_y_convertir(numero_str, base_origen, word_size):
    """
    Fase 1 y Fase 2:
    - Valida overflow contra el tamaño de palabra.
    - Aplica padding para completar el registro.
    - Devuelve el número simultáneamente en bin/oct/dec/hex.
    """
    valor_decimal = to_decimal(numero_str, base_origen)

    max_valor = (2 ** word_size) - 1
    if valor_decimal < 0 or valor_decimal > max_valor:
        raise OverflowError(
            f"Overflow / Desbordamiento de Registro: el valor {valor_decimal} "
            f"no cabe en {word_size} bits (máximo permitido: {max_valor})"
        )

    binario = from_decimal(valor_decimal, 2).zfill(bits_necesarios(word_size, 2))
    octal = from_decimal(valor_decimal, 8).zfill(bits_necesarios(word_size, 8))
    hexadecimal = from_decimal(valor_decimal, 16).zfill(bits_necesarios(word_size, 16))

    return {
        "binario": binario,
        "octal": octal,
        "decimal": str(valor_decimal),
        "hexadecimal": hexadecimal,
    }


def alu_operation(bin1, bin2, operacion, word_size):
    """
    Fase 3: ALU bit a bit (AND, OR, XOR) recorriendo índice por índice.
    """
    bin1 = bin1.strip().zfill(word_size)
    bin2 = bin2.strip().zfill(word_size)

    if len(bin1) > word_size or len(bin2) > word_size:
        raise OverflowError("Uno de los operandos excede el tamaño de palabra")

    for b in bin1 + bin2:
        if b not in ("0", "1"):
            raise ValueError("Los operandos deben ser cadenas binarias (0/1)")

    operacion = operacion.upper()
    resultado = []
    for i in range(word_size):
        d1 = int(bin1[i])
        d2 = int(bin2[i])
        if operacion == "AND":
            r = 1 if (d1 == 1 and d2 == 1) else 0
        elif operacion == "OR":
            r = 1 if (d1 == 1 or d2 == 1) else 0
        elif operacion == "XOR":
            r = 1 if d1 != d2 else 0
        else:
            raise ValueError(f"Operación no soportada: {operacion}")
        resultado.append(str(r))

    return "".join(resultado)
