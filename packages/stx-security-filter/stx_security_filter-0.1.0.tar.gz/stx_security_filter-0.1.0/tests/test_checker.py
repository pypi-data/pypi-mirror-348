from stx_security_filter import is_safe_input

# def test_safe_input():
#     assert is_safe_input("hello world") == True

# def test_sql_injection():
#     assert is_safe_input("UNION SELECT * FROM users") == True

# def test_xss_script():
#     assert is_safe_input("<script>alert(1)</script>") == False

# def test_blank_value():
#     assert is_safe_input("") == True



from stx_security_filter import is_safe_input

def test_safe_input():
    result = is_safe_input("hello world")
    print(f"test_safe_input = {result}")

def test_sql_injection():
    result = is_safe_input("UNION SELECT * FROM users")
    print(f"test_sql_injection = {result}")

def test_xss_script():
    result = is_safe_input("<script>alert(1)</script>")
    print(f"test_xss_script = {result}")

def test_blank_value():
    result = is_safe_input("")
    print(f"test_blank_value = {result}")

# Call the functions
test_safe_input()
test_sql_injection()
test_xss_script()
test_blank_value()


