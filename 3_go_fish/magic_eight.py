import random
def askQ():
    return str(input("What is your question? "))

answer=["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.",
"As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.",
"Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.",
"Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]


if __name__=="__main__":
    Q = askQ()
    while(Q != 'quit'):
        if(len(Q)<1 or Q[-1] != '?'):
            print("I’m sorry, I can only answer questions.")
        else:
            num=random.randint(0,19)
            print(answer[num])
        Q = askQ()
