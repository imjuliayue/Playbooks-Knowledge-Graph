from predicateExtractionFunctions import *

x = [['some x : everything, y : everything | Registrar[x] && DomainRegistration[y] && (Suspends[x,y] || Disables[x,y])', ['Registrar', 'DomainRegistration', 'Suspends', 'Disables'], ['x', 'y', 'x,y', 'x,y'], [' x is a registrar', ' y is a domain registration', ' x suspends y ', ' x disables y ']],
     ['some x : everything | Domain[x] && NoLongerUsedForMaliciousCommunications[x]', ['Domain', 'NoLongerUsedForMaliciousCommunications'], ['x', 'x'], [' x is a domain', ' x can no longer be used for malicious communications']]
]

saveData(x, 'test')

# openai_client()

# conditions = np.array([["D3-DRT-I1", "(input) The registrar suspends or disables the domain registration.","The process of performing a takedown of the attacker's domain registration infrastructure."],
# ["D3-DRT-I2", "(input) The domain can no longer be used for malicious communications such as C2 or phishing.","The process of performing a takedown of the attacker's domain registration infrastructure."],
# ["D3-DRT-SS3", "(system_state) An official abuse complaint is submitted to the registrar or host.","The process of performing a takedown of the attacker's domain registration infrastructure."],
# ["D3-DRT-SS4", "(system_state) Relevant government or intelligence agencies are informed for threat intelligence sharing.","The process of performing a takedown of the attacker's domain registration infrastructure."],
# ["D3-ER-I1", "(input) The email is deleted from storage and no longer accessible to the user.","The email removal technique deletes email files from system storage."]])

# result = batchExtraction(conditions)
# print(result)

# processed = processStringtoList(conditions, result)

# for x in processed:
#     print(x)