"""
Mini brainfuck (Inc0deus)
"""

c,s,l,d,p,q=open(input()).read(),[],{},[0]*30000,0,0
for i in range(len(c)):
 if c[i]=="[":s.append(i)
 if c[i]=="]":j=s.pop();l[j],l[i]=i,j
while q<len(c):
 i=c[q];p+=(i==">")-(i=="<");d[p]+=(i=="+")-(i=="-");j=d[p]
 if i==".":print(j)
 if i==",":d[p]=int(input())
 if (i=="[" and j==0)or(i=="]" and j>0):q=l[q]
 q+=1