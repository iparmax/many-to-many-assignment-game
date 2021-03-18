if idx == 1 :
    with open('results.dat', 'w') as f:
        f.write('Operator Optimal: \n')
        for item in z_star.items():
            if item[1] >=1:
                f.write(f'Path {item[0][1]} | Flow {item[1]} | Link Operated by {chr(item[0][2]+64)} | Price {str(round(price[item[0]],2))} \n')
        f.close
else:
    with open('results.dat', 'a') as f:
        f.write('User Optimal \n')
        for item in z_star.items():
            if item[1] >=1:
                f.write(f'Path {item[0][1]} | Flow {item[1]} | Link Operated by {chr(item[0][2]+64)} | Price {str(round(price[item[0]],2))} \n')
        f.close