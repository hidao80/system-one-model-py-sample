from openthai_systemone import SystemOneClient, Noul

# Customer needs to evaluate (label -> need text); each need is ranked against PRODUCTS separately
NEEDS = {
    "Developer": "I am a software developer who wants a free, highly customizable desktop for programming and server work, and I want to avoid license fees.",
    "Beginner": "I am looking for a device for web browsing and messaging.",
}

# Candidates to choose from (name -> description embedded in the question)
PRODUCTS = {
    "Windows": "the desktop operating system 'Windows'",
    "macOS": "the desktop operating system 'macOS'",
    "Linux Desktop": "the desktop operating system 'Linux Desktop'",
    "Android": "the mobile operating system 'Android'",
    "iOS/iPadOS": "the mobile operating system 'iOS/iPadOS'",
}

# automatically picks CUDA, MPS, or CPU
client = SystemOneClient("iapp/OpenThai-SystemOne")


def decision(state, options, question, yes, no):
    """Ask the same yes/no question about every option and return (name, p(yes)) pairs, best first.

    state:    any text or JSON-like dict the decision is based on
    options:  {name: description}
    question: question template; "{desc}" is replaced by each option's description
    yes / no: criteria templates; "{name}" is replaced by each option's name
    """
    resp = client.system_one(
        state=state,
        questions={
            name: Noul(
                instructions=question.format(desc=desc),
                criteria={"true": yes.format(name=name), "false": no.format(name=name)},
            )
            for name, desc in options.items()
        },
    )
    return sorted(((name, ans.noul) for name, ans in resp.answers.items()), key=lambda kv: kv[1], reverse=True)


for needs in NEEDS.values():
    for name, p in decision(
        state={"Customer's Request": needs},
        options=PRODUCTS,
        question="Does {desc} match the customer's needs?",
        yes="{name} is well suited to the customer's needs.",
        no="{name} is not suited to the customer's needs.",
    ):
        print(f"{name}: {p:.4f}")
