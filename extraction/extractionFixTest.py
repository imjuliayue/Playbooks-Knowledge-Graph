from predicateExtractionFunctions import *

openai_client()

conditions = np.array([["D3-DRT-I1", "(input) The registrar suspends or disables the domain registration.","The process of performing a takedown of the attacker's domain registration infrastructure."],
["D3-DRT-I2", "(input) The domain can no longer be used for malicious communications such as C2 or phishing.","The process of performing a takedown of the attacker's domain registration infrastructure."],
["D3-DRT-SS3", "(system_state) An official abuse complaint is submitted to the registrar or host.","The process of performing a takedown of the attacker's domain registration infrastructure."],
["D3-DRT-SS4", "(system_state) Relevant government or intelligence agencies are informed for threat intelligence sharing.","The process of performing a takedown of the attacker's domain registration infrastructure."],
["D3-ER-I1", "(input) The email is deleted from storage and no longer accessible to the user.","The email removal technique deletes email files from system storage."]])

result = batchExtraction(conditions)
print(result)


# result = ['[some x : everything, y : everything | Registrar[x] && DomainRegistration[y] && (Suspends[x,y] || Disables[x,y]),\n [Registrar; DomainRegistration; Suspends; Disables],\n [x; y; x,y; x,y],\n [ x is a registrar; y is a domain registration; x suspends y; x disables y ]\n]', '[all x : everything, w : everything | Domain[x] && MaliciousCommunication[w] implies not UsedFor[x,w],\n  [Domain; MaliciousCommunication; UsedFor],\n  [x; w; x,w],\n  [ x is a domain;  w is a malicious communication;  x is used for w ]\n]', '[some x : everything | AbuseComplaint[x] && ((some y : everything | Registrar[y] && SubmittedTo[x,y]) || (some z : everything | Host[z] && SubmittedTo[x,z])),\n  [AbuseComplaint; Registrar; Host; SubmittedTo],\n  [x; y; z; x,y; x,z],\n  [ x is an official abuse complaint; y is a registrar; z is a host; x is submitted to y; x is submitted to z ]\n]', '[all x : everything | Relevant[x] && (GovernmentAgency[x] || IntelligenceAgency[x]) implies (some y : everything | Informed[y,x]),\n [Relevant; GovernmentAgency; IntelligenceAgency; Informed],\n [x; x; x; y,x],\n [ x is relevant;  x is a government agency;  x is an intelligence agency;  y informs x ]\n]', '[some x : everything, y : everything, z : everything | Email[x] && Storage[y] && User[z] && DeletedFrom[x,y] && NoLongerAccessibleTo[x,z],\n [Email; Storage; User; DeletedFrom; NoLongerAccessibleTo],\n [x; y; z; x,y; x,z],\n [ x is an email;  y is a storage;  z is a user;  x is deleted from y;  x is no longer accessible to z ]\n]']

# print(string_to_list(result[0]))
# print(result[0])


processed = processStringtoList(conditions, result)

for x in processed:
    print(x)