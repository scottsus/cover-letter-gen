from generator import Generator

def main():
    gen = Generator()
    stream = gen.generate_cover_letter()
    
    for token in stream:
        print(token, end='', flush=True)
    print()

if __name__ == '__main__':
    main()
    