import timeit
import multiprocessing


# ============= Алгоритми ===================================

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            length = lps[length - 1] if length else 0
            if not length:
                lps[i] = 0
                i += 1
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            j = lps[j - 1] if j else 0
    return -1


def boyer_moore(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    skip = {ch: m - i - 1 for i, ch in enumerate(pattern[:-1])}
    i = 0
    while i <= n - m:
        j = m - 1
        while text[i + j] == pattern[j]:
            if j == 0:
                return i
            j -= 1
        i += skip.get(text[i + m - 1], m)
    return -1


def rabin_karp(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    h = pow(d, m-1) % q
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for s in range(n - m + 1):
        if p == t and text[s:s + m] == pattern:
            return s
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q
    return -1


# ============ Зчитування тексту з файла ================

def read_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
        return ''


# ============ Безпечний запуск з таймаутом =============

def safe_run(algo, text, pattern, return_dict):
    start = timeit.default_timer()
    try:
        index = algo(text, pattern)
        past = timeit.default_timer() - start
        return_dict["index"] = index
        return_dict["past"] = past
    except Exception as e:
        return_dict["error"] = str(e)


# ============ Запускаємо тест ==========================

def run_test(label, text, existing_sub, non_existing_sub):
    print(f"\n===== {label} =====")
    print(f"{'Алгоритм':15} | {'Підрядок':10} | {'Час':>10} | Результат")

    for name, algo in {
        'KMP': kmp_search,
        'Boyer-Moore': boyer_moore,
        'Rabin-Karp': rabin_karp
    }.items():
        for case_label, pattern in [('Існує', existing_sub), ('Не існує', non_existing_sub)]:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            p = multiprocessing.Process(
                target=safe_run, args=(algo, text, pattern, return_dict))
            p.start()
            p.join(5)  # таймаут — 5 секунд

            if p.is_alive():
                p.terminate()
                print(
                    f"{name:15} | {case_label:10} | -----    | Зависання (>5 сек)")
            elif "error" in return_dict:
                print(
                    f"{name:15} | {case_label:10} | -----    | Помилка: {return_dict['error']}")
            else:
                idx = return_dict["index"]
                past = return_dict["past"]
                if idx != -1:
                    position_type = (
                        "початок" if idx < len(text) * 0.33 else
                        "середина" if idx < len(text) * 0.66 else
                        "кінець"
                    )
                    print(
                        f"{name:15} | {case_label:10} | {past:.6f} сек | Знайдено ({position_type}, позиція {idx})")
                else:
                    print(
                        f"{name:15} | {case_label:10} | {past:.6f} сек | Не знайдено")


# ============ Основна частина ==========================

if __name__ == "__main__":
    path_1 = "text/article_1.txt"
    path_2 = "text/article_2.txt"

    text_1 = read_text(path_1)
    text_2 = read_text(path_2)

    existing_substring_1 = "комп'ютерних наук"
    non_existing_substring_1 = "несуществующий текст"

    existing_substring_2 = "Искусство программирования"
    non_existing_substring_2 = "текст не найден"

    run_test("Стаття 1", text_1, existing_substring_1,
             non_existing_substring_1)
    run_test("Стаття 2", text_2, existing_substring_2,
             non_existing_substring_2)
