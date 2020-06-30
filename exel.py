import json

out = open('g_data.txt')
s = json.load(out)
dict_s = dict(s)
print("Enter scores:")
gain_s = {}
kick_ls = {}
for n, sc in dict_s.items():
    gp_score = input("{}: ".format(n))
    gain = int(gp_score)-int(sc)
    dict_s.update({n: gp_score})
    gain_s.update({n: gain})
    if gain < 1000:
        kick_ls.update({n: gain})
    with open('gain_list.txt', 'w') as gl:
        json.dump(gain_s, gl)
    with open('g_data.txt', 'w') as gp:
        json.dump(dict_s, gp)
    with open('k_list.txt', 'w') as kl:
        json.dump(kick_ls, kl)
