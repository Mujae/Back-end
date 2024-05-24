package skhu.skhuadventure;


import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TestService {
    @Autowired
    MemberRepository memberRepository;

    public List<Member> getAllMembers(){
        return memberRepository.findAll();
    }
}
