from docemul.generator import generate

def run(dir, num=5, size=None, sampler=None, greyscale=False,type='TXT',model='branden2.xml',seed=2):
    generate(dir, num=num, size=size,sampler=sampler, greyscale=greyscale,type=type,model=model,seed=seed)


run('GENERATED/Brandenburg/test')



